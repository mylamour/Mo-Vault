import os
import uuid
import pkcs11

ALGS= ["aes","rsa"]
PKCS11_MODULE=os.environ["PKCS11_MODULE"]
os.environ["PKCS11_PROXY_SOCKET"]="tls://172.17.0.2:5657"
os.environ["PKCS11_PROXY_TLS_PSK_FILE"]="TLS-PSK"


def login(token,pin):
    pass

def init_key():
    pass

def encrypt(alg, slot, token=None, token_label=None):
    #type: symmetric / asymmetry
    # alg
    if alg in ALGS:
        pass

    return "We don't support this algorithms yet"


def decrypt():
    pass