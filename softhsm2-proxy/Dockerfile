
FROM softhsm2-proxy:base
LABEL maintainer "Mour <mylamour@163.com>"

ARG HSM_KEYSHARES
ARG HSM_KEY_THESHOLD
ARG MY_TOKENLABLE
ARG MY_PKCS11_PROXY_PORT

ENV HSM_KEYSHARES=$HSM_KEYSHARES
ENV HSM_KEY_THESHOLD=$HSM_KEY_THESHOLD
ENV TOKENLABLE=$MY_TOKENLABLE
ENV PKCS11_PROXY_PORT=$MY_PKCS11_PROXY_PORT


# Protected the Pin With PGP Key
# Please change it to your own public key and recipient 
ENV SOFTHSM2_CONF="/root/softhsm2.conf"
ENV PIN_PRO_PGP_PUBLICKEYS_DIR="/opt/publickeys/"
# ENV PGP_RECIPIENT="PIN_PRO"
ENV PIN_SECRET="/tmp/pinsecret"
ENV PIN_SECRET_PGP="/tmp/pinsecret.gpg"
ENV SO_PIN_SECRET="/tmp/sopinsecret"
ENV SO_PIN_SECRET_PGP="/tmp/sopinsecret.gpg"
ENV SSS_COMBINE="/usr/local/bin/secret-share-combine"
ENV SSS_SPLIT="/usr/local/bin/secret-share-split"

# For PKCS#11 Proxy Services
# ENV PKCS11_PROXY_PORT=5657
# # ENV PKCS11_DAEMON_SOCKET="tcp://0.0.0.0:5657"
ENV PKCS11_MODULE="/usr/local/lib/softhsm/libsofthsm2.so"
ENV PKCS11_DAEMON_SOCKET="tls://0.0.0.0:${PKCS11_PROXY_PORT}"
ENV PKCS11_PROXY_TLS_PSK_FILE="/root/TLS-PSK"
# EXPOSE ${PKCS11_PROXY_PORT}

#  It's better to working with mount for token directorys

COPY web/ /root/
RUN pip3 install -r /root/requirements.txt -i https://pypi.doubanio.com/simple

COPY publickeys/* ${PIN_PRO_PGP_PUBLICKEYS_DIR}
COPY softhsm2.conf /root/softhsm2.conf
COPY start.sh /root/start.sh
COPY TLS-PSK ${PKCS11_PROXY_TLS_PSK_FILE}
COPY sss/secret-share-combine ${SSS_COMBINE}
COPY sss/secret-share-split ${SSS_SPLIT}
RUN chmod a+x /root/start.sh
ENTRYPOINT [ "bash","/root/start.sh" ]
