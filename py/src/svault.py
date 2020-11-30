from uuid import uuid4

from .utils import string_to_bytes, bytes_to_string, bytes_to_hex, hex_to_bytes
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

class Svault:

    def __init__(self, secret):
        
        self.secret = secret
        self.key_type = self.secret.key_type.name

    def encrypt(self, plaintext,iv=None):
        if self.key_type == "AES" :
            if not iv:
                iv = aes_key_iv =uuid4().hex
            ciphertext = self.secret.encrypt(plaintext, mechanism_param=hex_to_bytes(aes_key_iv))
                
            return iv, ciphertext.hex()
        
        if self.key_type == "RSA" :
            ciphertext = self.secret.encrypt(plaintext)
            print(ciphertext)
            return None, ciphertext.hex()

    def decrypt(self,ciphertext,iv=None):
        if self.key_type == "AES":
            plaintext = self.secret.decrypt(ciphertext, mechanism_param=hex_to_bytes(iv))
            return plaintext


        if self.key_type == "RSA":
            plaintext = self.secret.decrypt(ciphertext, mechanism=Mechanism.RSA_PKCS)
            return plaintext

    def sign(self,payload):
        if self.key_type == "RSA":
            signautre = self.secret.sign(payload)
            return signautre


    def verify(self,payload,signautre):
        if self.key_type == "RSA":
            sameornot = self.secret.verify(string_to_bytes(payload), signautre)
            return sameornot

    def wrap(self):
        pass

    def unwrap(self):
        pass

    def digest(self):
        pass

    def hash(self):
        pass

    def x509(self):
        pass




if __name__ == "__main__":
    pass