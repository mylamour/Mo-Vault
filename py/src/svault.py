import os
import logging
import uuid
import pkcs11
from pkcs11 import KeyType,Attribute
from pkcs11 import Mechanism
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
        self.token = token
        self.key = None
        self.lib = pkcs11.lib(PKCS11_PROXY_MODULE)
        # self.lib = pkcs11.lib("/usr/local/lib/softhsm/libsofthsm2.so")

        self.slot = self.lib.get_token(token_label=slot)

        self.symmetric = []
        self.asymmetric = []

        # key_version should be byte type
        self.key_version = '0'.encode()
        self.aes_key_iv = None

        if version:
            self.key_version = str(version).encode()
        

        # try:
        self.session=self.slot.open(user_pin=pin)

        if self.token:
            self.get_token()
            print(self.key)
            self.key_version = str(int.from_bytes(self.key.id,"big") + 1).encode()


        # except PinIncorrect:
        #     logging.info("PIN was error")
        # except NoSuchToken:
        #     logging.info("TOKEN was not exists")


    def init_key(self,alg,token):

        if alg.lower() == "aes":

            self.token=token

            self.key = self.session.generate_key(KeyType.AES, 128, template={
                Attribute.SENSITIVE: False,
                Attribute.EXTRACTABLE: False,
                Attribute.LABEL: self.token,
                Attribute.ID: self.key_version
                })

        if alg.lower() == "des":
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


    # data = b'人间忽晚，山河已秋'.encode('utf-8')

    data = b'You are handsome'

    mtoken = str(uuid.uuid1()).replace('-','')

    hsm = HSM(slot="OpenDNSSEC",pin="1234")
    hsm.init_key('aes', mtoken)
    print(hsm.key)
    
    ciphertext = hsm.encrypt(data)
    iv = hsm.aes_key_iv


    print(ciphertext)

    hsm.logout()

    
    hsm2 = HSM(slot="OpenDNSSEC",pin="1234", token=mtoken)
    plaintext = hsm2.decrypt(ciphertext,iv)


    print(plaintext)