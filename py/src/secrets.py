import os
import uuid
import pkcs11
import logging

from utils import bytes_to_hex, hex_to_bytes, int_to_bytes, bytes_to_int, tree

from subprocess import Popen,PIPE
from shamirss import PlaintextToHexSecretSharer
from pkcs11 import Mechanism, KeyType, Attribute
from pkcs11.exceptions import PinIncorrect, NoSuchKey, NoSuchToken, MultipleObjectsReturned

ALGS= ["aes","rsa"]

PKCS11_PROXY_MODULE=os.environ.get("PKCS11_PROXY_MODULE")
PKCS11_MODULE=os.environ.get("PKCS11_MODULE")
PKCS11_PROXY_SOCKET=os.environ.get("PKCS11_PROXY_SOCKET")
PKCS11_PROXY_TLS_PSK_FILE=os.environ.get("PKCS11_PROXY_TLS_PSK_FILE")

# /usr/local/lib/softhsm/libsofthsm2.so
# /usr/local/lib/libpkcs11-proxy.so

class HSM(object):

    def __init__(self, slot, pin, token=None, version=None):
        """ 
        slot(uuid user) -> RSA key -> RSA key version
           - slot was slot label 
           - token was key label
        """
            
        if not PKCS11_MODULE:
            raise Exception("Didn't find the PKCS11_MODULE")
        
        if not PKCS11_PROXY_MODULE:
            raise Exception("Didn't find PKCS11_PROXY_MODULE")

        if not PKCS11_PROXY_SOCKET:
            raise Exception("Didn't find the PKCS11_PROXY_SOCKET")

        if not PKCS11_PROXY_TLS_PSK_FILE:
            raise Exception("Didn't find the PKCS11_PROXY_TLS_PSK_FILE")

        self.session = None
        self.token = None
        self.pin = pin
        self.token = token   # uuid for the 
        self.key = None
        self.lib = pkcs11.lib(PKCS11_PROXY_MODULE)
        # self.lib = pkcs11.lib("/usr/local/lib/softhsm/libsofthsm2.so")

        self.slot = self.lib.get_token(token_label=slot)

        self.symmetric = tree()
        self.asymmetric = tree()

        # key_version should be byte type
        self.key_version = int_to_bytes(1)

        if version:
            self.key_version = int_to_bytes(version)
        
        try:
            self.session=self.slot.open(user_pin=pin, rw=True)
            #  Once initialized, it would be only once.
            self.init_root() 
        except PinIncorrect:
            logging.info("PIN was error")
        except NoSuchToken:
            logging.info("TOKEN was not exists")

        if self.token:
            self.get_token()
            self.key_version = int_to_bytes(self.key_version+1)


    def init_root(self):
        if self.session.get_key(label="_ROOT_LMK_", id=self.key_version):
            pass
        else:
            self.session.generate_keypair(pkcs11.KeyType.RSA, 4096, store=True, label='_ROOT_LMK_')

    def gen_aes(self, token, version):
        self.token = token

        return self.session.generate_key(KeyType.AES, 128, store=True, template={
            Attribute.SENSITIVE: True,
            Attribute.EXTRACTABLE: True,
            Attribute.LABEL: self.token,
            Attribute.ID: self.key_version
        })


        #  step 1:
        # "{}-{}".format(oneapp_aes_test[Attribute.VALUE].hex(), iv.hex())
        # oneapp_pub.encrypt("{}-{}".format(oneapp_aes_test[Attribute.VALUE].hex(), iv.hex())).hex()
        # 

    def gen_rsa(self, token, version):
        self.session.generate_keypair(pkcs11.KeyType.RSA, 2048, store=True, label=token)


    def init_key(self,alg,token=None):

        if alg.lower() == "aes":
            pass
            # aes = self.gen_aes(token=token)
            


        if alg.lower() == "rsa":
            pass

        if alg.lower() == "":
            pass

        return "We don't support this algorithms yet"

    def get_token(self):

        try:
            self.key = self.session.get_key(label=self.token, id=self.key_version)
        except NoSuchKey:
            pass
        except MultipleObjectsReturned:
            pass

    def logout(self):
        self.session.close()

    def encrypt(self,plaintext,iv=None):
        #type: symmetric / asymmetry
        # alg

        ciphertext = None
        
        if self.key.key_type.name == "AES" :

            if not iv:
                self.aes_key_iv = self.session.generate_random(128)
                ciphertext = self.key.encrypt(plaintext, mechanism_param=self.aes_key_iv)
               
            else:
                ciphertext = self.key.encrypt(plaintext,  mechanism_param=iv)

        if self.key.key_type.name == "DES3" :
            pass

        return ciphertext


    def decrypt(self, ciphertext, iv=None):
        if self.key.key_type.name == "AES":
            if iv:
                return self.key.decrypt(ciphertext, mechanism_param=iv)
            # return self.key.encrypt(ciphertext,mechanism=Mechanism.AES_OFB,mechanism_param=self.aes_key_iv)

    
    def sign(self):
        pass

    def verify(self):
        pass

    def plaintext(self):
        pass

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
        
    hsm = HSM(slot="OpenDNSSEC", pin="4dae441c0d1614ff93cc47eb414af2b919d9e28d99e9699c8b09a4e6483f48c1")