from utils import string_to_bytes, bytes_to_hex

from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.util.rsa import encode_rsa_public_key

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5

class Svault:

    def __init__(self, secret):
        pass

    def import_secret(self):
        pass

    def export_secret(self):
        pass



    def encrypt(self, secret, plaintext) :
        # # Extract public key
        # key = session.get_key(label="Mo", key_type=KeyType.RSA, object_class=ObjectClass.PUBLIC_KEY)

        if secret == "aes":
            pass

        if secret == "rsa":
            key = RSA.importKey(encode_rsa_public_key(secret))
            # Encryption on the local machine
            cipher = Cipher_PKCS1_v1_5.new(key)
            crypttext = cipher.encrypt(string_to_bytes(plaintext))

            return bytes_to_hex(crypttext)

    def decrypt(self, secret, ciphertext):
        if secret == "aes":
            pass

        if secret == "rsa":
            pass
            # priv = session.get_key(label="Mo", key_type=KeyType.RSA, object_class=ObjectClass.PRIVATE_KEY)
            # plaintext = priv.decrypt(crypttext, mechanism=Mechanism.RSA_PKCS)

    def sign(self):
        pass

    def verify(self):
        pass

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