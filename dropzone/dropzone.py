import os
import json
import logging
import requests

from pyftpdlib.authorizers import UnixAuthorizer, DummyAuthorizer
from pyftpdlib.filesystems import UnixFilesystem
from pyftpdlib.handlers import FTPHandler, TLS_FTPHandler
from pyftpdlib.servers import FTPServer

SECRET_PATH = "random_test/rsa"
SECRET_VERSION = "2"


class Dropzone(FTPHandler):
    def on_connect(self):
        print("%s:%s connected" % (self.remote_ip, self.remote_port))

    def on_disconnect(self):
        # do something when client disconnects
        pass

    def on_login(self, username):
        # do something when user login
        pass

    def on_logout(self, username):
        # do something when user logs out
        pass

    def on_file_sent(self, file):
        # do something when a file has been sent
        data = {"secret_path": SECRET_PATH, "secret_version": SECRET_VERSION, "ciphertext": open(file, 'rb').read().decode("utf-8")}

        response = requests.post(
            'http://127.0.0.1:8443/key/decrypt/rsa', json=data)

        with open(file, 'w') as f:
            f.write(json.dumps(response.text)['plaintext'])

    def on_file_received(self, file):

        data = {"secret_path": "{}".format(
            SECRET_PATH), "secret_version": SECRET_VERSION, "plaintext": "{}".format(open(file, 'rb').read())}

        response = requests.post(
            'http://127.0.0.1:8443/key/encrypt/rsa', json=data)

        with open(file, 'w') as f:
            f.write(json.loads(response.text)['ciphertext'])

    def on_incomplete_file_sent(self, file):
        # do something when a file is partially sent
        pass

    def on_incomplete_file_received(self, file):
        # remove partially uploaded files
        os.remove(file)


def main():
    # authorizer = UnixAuthorizer(rejected_users=["root"],
    #                             require_valid_shell=True)
    authorizer = DummyAuthorizer()

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    # os.getcwd()
    authorizer.add_user('user', '12345', os.getcwd(), perm='elradfmwMT')
    authorizer.add_anonymous(os.getcwd())

    # Instantiate FTP handler class
    handler = Dropzone
    handler.authorizer = authorizer

    # handler.certfile = 'keycert.pem'
    # handler.tls_control_required = True
    # handler.tls_data_required = True

    # Define a customized banner (string returned when client connects)
    handler.banner = "Share your data with dropzone."

    handler.passive_ports = range(60000, 65535)

    handler.abstracted_fs = UnixFilesystem
    server = FTPServer(('', 2121), handler)
    server.serve_forever()


if __name__ == "__main__":
    main()
