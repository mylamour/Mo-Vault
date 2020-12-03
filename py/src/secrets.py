import os
import uuid
import pkcs11
import logging

from .utils import bytes_to_hex, hex_to_bytes, int_to_bytes, bytes_to_int, tree

from subprocess import Popen, PIPE
# from shamirss import PlaintextToHexSecretSharer
from pkcs11 import Mechanism, KeyType, Attribute, ObjectClass
from pkcs11.exceptions import PinIncorrect, NoSuchKey, NoSuchToken, MultipleObjectsReturned, UserAlreadyLoggedIn

ALGS = ["aes", "rsa"]

PKCS11_PROXY_MODULE = os.environ.get("PKCS11_PROXY_MODULE")
PKCS11_MODULE = os.environ.get("PKCS11_MODULE")
PKCS11_PROXY_SOCKET = os.environ.get("PKCS11_PROXY_SOCKET")
PKCS11_PROXY_TLS_PSK_FILE = os.environ.get("PKCS11_PROXY_TLS_PSK_FILE")

# /usr/local/lib/softhsm/libsofthsm2.so
# /usr/local/lib/libpkcs11-proxy.so


class HSM(object):
    SESSION = None
    def __init__(self, slot, pin):
        """ 
        slot(uuid user) -> RSA key -> RSA key version
           - slot was slot label 
           - pin was used to login into slot
           - secret_path was key path, eg: app/qa/order/rsa/nucc_test
           - secret_version was key version. range: 1-N
        """

        # if not PKCS11_MODULE:
        #     raise Exception("Didn't find the PKCS11_MODULE")

        # if not PKCS11_PROXY_MODULE:
        #     raise Exception("Didn't find PKCS11_PROXY_MODULE")

        # if not PKCS11_PROXY_SOCKET:
        #     raise Exception("Didn't find the PKCS11_PROXY_SOCKET")

        # if not PKCS11_PROXY_TLS_PSK_FILE:
        #     raise Exception("Didn't find the PKCS11_PROXY_TLS_PSK_FILE")

        self.session = None
        self.pin = pin

        # if secret_version and secret_path:
        #     self.secret_path = secret_path
        #     self.secret_version = int_to_bytes(secret_version)

        # self.lib = pkcs11.lib(PKCS11_PROXY_MODULE)
        self.lib = pkcs11.lib("/usr/local/lib/softhsm/libsofthsm2.so")

        self.slot = self.lib.get_token(token_label=slot)

        self.symmetric = tree()
        self.asymmetric = tree()

        try:
            self.session = self.slot.open(user_pin=pin, rw=True)
            HSM.SESSION = self.session
        except PinIncorrect:
            logging.info("PIN was error")
        except NoSuchToken:
            logging.info("slot was not exists")
        except UserAlreadyLoggedIn:
            logging.info("slot was already login, let me close it and login again")

    # def init_root(self):
    #     if self.session.get_key(label="_ROOT_LMK_", id=self.key_version):
    #         pass
    #     else:
    #         self.session.generate_keypair(pkcs11.KeyType.RSA, 4096, store=True, label='_ROOT_LMK_')

    def get_aes(self, secret_path, secret_version):
        try:
            aes_key = self.session.get_key(
                label=secret_path, id=int_to_bytes(secret_version))
            return aes_key
        except NoSuchKey:
            logging.error("No Such Key")

    def get_rsa(self, secret_path, secret_version,keypairs=None):
        
        pub = self.session.get_key(label=secret_path, id=int_to_bytes(secret_version), key_type=KeyType.RSA, object_class=ObjectClass.PUBLIC_KEY)
        priv = self.session.get_key(label=secret_path, id=int_to_bytes(secret_version), key_type=KeyType.RSA, object_class=ObjectClass.PRIVATE_KEY)

        if keypairs == "public":
            return pub
        if keypairs == "private":
            return priv
            
        return pub, priv

    def gen_aes(self, secret_path, secret_version, secret_len=128, extract=False):
        """
            create key when it not exists
        """

        try:
            tmp_aes = self.session.get_key(label=secret_path, id=int_to_bytes(secret_version))
            if tmp_aes:
                return False

        except NoSuchKey:
            if secret_path and secret_version:
                    self.session.generate_key(KeyType.AES, secret_len, store=True, template={
                        Attribute.SENSITIVE: True, 
                        Attribute.EXTRACTABLE: extract,
                        Attribute.LABEL: secret_path,
                        Attribute.ID: int_to_bytes(secret_version)})
                    return True
        return False

    def gen_rsa(self, secret_path, secret_version, secret_len=2048):
        """
            create key when it not exists
        """
        try:
            tmp_public = self.session.get_key(label=secret_path, id=int_to_bytes(
                secret_version), key_type=KeyType.RSA, object_class=ObjectClass.PUBLIC_KEY)
            if tmp_public:
                return False
        except NoSuchKey:
            if secret_path and secret_version:
                self.session.generate_keypair(
                    KeyType.RSA, secret_len, store=True, label=secret_path, id=int_to_bytes(secret_version))
                return True

        return False

    def rotate_aes(self, secret_path, secret_version, extract=False):

        try:
            tmp = self.session.get_key(label=secret_path, id=int_to_bytes(
                secret_version), key_type=KeyType.RSA)
            if tmp:
                # int_to_bytes(bytes_to_int(tmp.id)+1)
                self.session.generate_key(KeyType.AES, 128, store=True, template={
                    Attribute.SENSITIVE: True,
                    Attribute.EXTRACTABLE: extract,
                    Attribute.LABEL: secret_path,
                    Attribute.ID: secret_version})

        except NoSuchKey:
            logging.error("You can't rotate a key which not exists")

    def rotate_rsa(self, secret_path, secret_version):
        """
            - need to create a function to pkcs11 lib with get_keys
        """
        try:
            tmp = self.session.get_key(label=secret_path, id=int_to_bytes(
                secret_version), key_type=KeyType.RSA, object_class=ObjectClass.PUBLIC_KEY)
            if tmp:
                # int_to_bytes(bytes_to_int(tmp.id)+1)
                self.session.generate_keypair(
                    KeyType.RSA, tmp.key_length, store=True, label=secret_path, id=int_to_bytes(secret_version+1))

        except NoSuchKey:
            logging.error("You can't rotate a key which not exists")

    def destory(self):
        """
            self.session.get_key and destory if it's a pub key and privat key 
        """
        pass

    def logout(self):
        self.session.close()


if __name__ == "__main__":

    # output = StringIO()
    # import tempfile
    # import mmap

    # with tempfile.NamedTemporaryFile() as f:
    #     f.write("039b1b9671b5963f746050819170c290b833d5fec1fdde4c6b3bf5e3cb35f72323e62259334e908dc84628e64e490f7c4743911f10f88ae2669afd1e922ff05eceac8bfd321f146a4ae6899fdd4973b0693388bffd1c21c4a87ea2cec0a0a90a99cd101f936bd2f1f393e9df43fc1f7d449c".encode("utf-8"))
    #     f.write("028e9a9707106c5702000c527f4712f156f44f615d6f2a761f1dff1785b5e025a5e62259334e908dc84628e64e490f7c4743911f10f88ae2669afd1e922ff05eceac8bfd321f146a4ae6899fdd4973b0693388bffd1c21c4a87ea2cec0a0a90a99cd101f936bd2f1f393e9df43fc1f7d449c".encode("utf-8"))
    #     f.write("01b102949de479ef98a0e83c561e79527fa6fadbe2c22d388377e110572ed92f34e62259334e908dc84628e64e490f7c4743911f10f88ae2669afd1e922ff05eceac8bfd321f146a4ae6899fdd4973b0693388bffd1c21c4a87ea2cec0a0a90a99cd101f936bd2f1f393e9df43fc1f7d449c".encode("utf-8"))

    #     print(f.name)
    #     p2 = Popen(["cat", f.name, "| ../softhsm2-proxy/sss/secret-share-combine"],stdout=PIPE,stderr=PIPE)
    #     result = p2.stdout.read().decode("utf-8").strip('\n')
    pass