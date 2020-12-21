
FROM softhsm2-proxy:base
LABEL maintainer "Mour <mylamour@163.com>"

ARG HSM_KEYSHARES
ARG HSM_KEY_THESHOLD
ARG MY_TOKENLABEL
ARG MY_PKCS11_PROXY_PORT

ENV HSM_KEYSHARES=$HSM_KEYSHARES
ENV HSM_KEY_THESHOLD=$HSM_KEY_THESHOLD
ENV TOKENLABEL=$MY_TOKENLABEL
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
ENV PKCS11_PROXY_TLS_PSK_FILE="/eaas/TLS-PSK"
# EXPOSE ${PKCS11_PROXY_PORT}

#  It's better to working with mount for token directorys

COPY publickeys/* ${PIN_PRO_PGP_PUBLICKEYS_DIR}
COPY softhsm2.conf /root/softhsm2.conf

COPY web/ /eaas/
RUN pip3 install -r /eaas/requirements.txt -i https://pypi.doubanio.com/simple

COPY TLS-PSK ${PKCS11_PROXY_TLS_PSK_FILE}
COPY sss/secret-share-combine ${SSS_COMBINE}
COPY sss/secret-share-split ${SSS_SPLIT}

COPY start.sh /eaas/start.sh
RUN chmod a+x /eaas/start.sh
ENTRYPOINT [ "bash","/eaas/start.sh" ]
