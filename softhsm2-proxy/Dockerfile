
FROM softhsm2-proxy:base
LABEL maintainer "Mour <mylamour@163.com>"

ARG MY_PGP_PUBLIC_KEY_NAME
ARG MY_PGP_RECIPIENT
ARG MY_TOKENLABLE
ARG MY_PKCS11_PROXY_PORT


ENV PGP_PUBLIC_KEY_NAME=$MY_PGP_PUBLIC_KEY_NAME
ENV TOKENLABLE=$MY_TOKENLABLE
ENV PGP_RECIPIENT=$MY_PGP_RECIPIENT
ENV PKCS11_PROXY_PORT=$MY_PKCS11_PROXY_PORT


# Protected the Pin With PGP Key
# Please change it to your own public key and recipient 
ENV SOFTHSM2_CONF="/root/softhsm2.conf"
ENV PIN_PRO_PGP_PUBLICKEY="/root/public.asc"
# ENV PGP_RECIPIENT="PIN_PRO"
ENV PIN_SECRET="/tmp/pinsecret"
ENV PIN_SECRET_PGP="/tmp/pinsecret.gpg"
ENV SO_PIN_SECRET="/tmp/sopinsecret"
ENV SO_PIN_SECRET_PGP="/tmp/sopinsecret.gpg"


# For PKCS#11 Proxy Services
# ENV PKCS11_PROXY_PORT=5657
# # ENV PKCS11_DAEMON_SOCKET="tcp://0.0.0.0:5657"
ENV PKCS11_DAEMON_SOCKET="tls://0.0.0.0:${PKCS11_PROXY_PORT}"
ENV PKCS11_PROXY_TLS_PSK_FILE="/root/TLS-PSK"

# EXPOSE ${PKCS11_PROXY_PORT}

#  It's better to working with mount for token directorys

COPY ${PGP_PUBLIC_KEY_NAME} ${PIN_PRO_PGP_PUBLICKEY}
COPY softhsm2.conf /root/softhsm2.conf
COPY start.sh /root/start.sh
COPY TLS-PSK ${PKCS11_PROXY_TLS_PSK_FILE}

RUN chmod a+x /root/start.sh
ENTRYPOINT [ "sh","/root/start.sh" ]
