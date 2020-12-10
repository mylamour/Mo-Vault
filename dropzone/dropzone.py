import os
import json
import logging
import requests
import hashlib

from fs.osfs import OSFS
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from pyftpdlib.authorizers import UnixAuthorizer, DummyAuthorizer
from pyftpdlib.filesystems import UnixFilesystem
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer, MultiprocessFTPServer

SECRET_PATH = "random_test/rsa"
SECRET_VERSION = "2"
EAAS_HOST = "http://127.0.0.1"
EAAS_PORT = "8443"
CERTFILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"keycert.pem"))

TLS = False

def key_decrypt(ciphertext):
    data = {"secret_path": SECRET_PATH, "secret_version": SECRET_VERSION, "ciphertext": ciphertext}

    response = requests.post('{}:{}/key/decrypt/rsa'.format(EAAS_HOST, EAAS_PORT), json=data)

    return json.loads(response.text)['plaintext']

def key_encrypt(plaintext):
    data = {"secret_path": "{}".format(
        SECRET_PATH), "secret_version": SECRET_VERSION, "plaintext":plaintext}

    response = requests.post('{}:{}/key/encrypt/rsa'.format(EAAS_HOST, EAAS_PORT), json=data)

    
    return json.loads(response.text)['ciphertext']


class Dropzone(TLS_FTPHandler):


    key = None
    kek_path = None
    key_size=256
    home_dir = None

    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        pass

    def on_login(self, username):
        self.kek_path = "keks/.{}.secret".format(hashlib.sha224(username.encode('utf-8')).hexdigest())
        self.home_dir = "remote/{}".format(username)

        if not os.path.isdir(self.home_dir):
            os.mkdir(self.home_dir)

        if os.path.exists(self.kek_path):
            self.key = bytes.fromhex(key_decrypt(open(self.kek_path,'r').read()))
            os.remove(self.kek_path)
        
            for path, _, files in os.walk(self.home_dir):
                for name in files:
                    if name.endswith(".enc"):
                        self.decrypt_file(os.path.join(path, name))
                        os.remove(os.path.join(path, name))

    def on_logout(self, username):
        self.key = get_random_bytes(32)
        flag = True

        for path, _, files in os.walk(self.home_dir):
            for name in files:
                if not name.endswith(".enc"):
                    self.encrypt_file(os.path.join(path, name))
                    os.remove(os.path.join(path, name))
                else:
                    flag = False

        if flag:
            # byter-> to string
            with open(self.kek_path, 'w') as f:
                f.write(key_encrypt(self.key.hex()))


    def on_file_sent(self, file):
        pass

    def on_file_received(self, file):
        pass


    def on_incomplete_file_sent(self, file):
        pass

    def on_incomplete_file_received(self, file):
        os.remove(file)

    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt(self, message):
        message = self.pad(message)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    def decrypt(self, ciphertext):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)

    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)


def main():
    # authorizer = UnixAuthorizer(rejected_users=["root"],
    #                             require_valid_shell=True)
    authorizer = DummyAuthorizer()
    handler = Dropzone

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    # os.getcwd()
    username = 's'
    password = 's'

    home_dir = "remote/s"
    
    authorizer.add_user(username, password, home_dir, perm='elradfmwMT')
    # authorizer.add_anonymous()

    handler.authorizer = authorizer
    handler.certfile = CERTFILE

    if TLS:
        handler.tls_control_required = True
        handler.tls_data_required = True

    # Define a customized banner (string returned when client connects)
    handler.banner = "Share your data with dropzone."

    handler.passive_ports = range(60000, 65535)

    handler.abstracted_fs = UnixFilesystem
    server = MultiprocessFTPServer(('', 2121), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()