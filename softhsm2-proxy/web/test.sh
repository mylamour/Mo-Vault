#!/bin/bash

server_tls(){
    export 
    export PKCS11_MODULE=/usr/local/lib/softhsm/libsofthsm2.so
    export PKCS11_DAEMON_SOCKET=tls://127.0.0.1:5657
    export PKCS11_PROXY_TLS_PSK_FILE=/home/ian/Desktop/Mo-softhsm/py/src/TLS-PSK
    /usr/local/bin/pkcs11-daemon /usr/local/lib/softhsm/libsofthsm2.so
}

# /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so
# /usr/local/lib/libpkcs11-proxy.so

client_tls(){
    export PKCS11_PROXY_TLS_PSK_FILE=/home/ian/Desktop/Mo-softhsm/py/src/TLS-PSK
    export PKCS11_PROXY_SOCKET=tls://127.0.0.1:5657
    export PKCS11_PROXY_MODULE=/home/ian/Desktop/Mo-softhsm/py/pkcs11-proxy/libpkcs11-proxy.so
    # pkcs11-tool --module=/usr/local/lib/libpkcs11-proxy.so -L
    python3 app.py
}

server_tcp(){
    export PKCS11_MODULE=/usr/local/lib/softhsm/libsofthsm2.so
    export PKCS11_DAEMON_SOCKET=tcp://127.0.0.1:5657
    /usr/local/bin/pkcs11-daemon /usr/local/lib/softhsm/libsofthsm2.so
}

# /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so
# /usr/local/lib/libpkcs11-proxy.so

client_tcp(){
    export PKCS11_PROXY_SOCKET=tcp://127.0.0.1:5657
    export PKCS11_PROXY_MODULE=/home/ian/Desktop/Mo-softhsm/py/pkcs11-proxy/libpkcs11-proxy.so
    # pkcs11-tool --module=/usr/local/lib/libpkcs11-proxy.so -L
    python3 app.py
}