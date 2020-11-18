FROM ubuntu:latest
LABEL maintainer "Mour <mylamour@163.com>"

ENV LANG=en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV SOFTHSM2_CONF="/root/softhsm2.conf"
ENV TOKENLABLE="DEMO"

# Protected the Pin With PGP Key
ENV PIN_PRO_PGP_PUBLICKEY="/tmp/PIN_PRO.testing.public.asc"
ENV PGP_RECIPIENT="PIN_PRO"
ENV PIN_SECRET="/tmp/pinsecret"
ENV PIN_SECRET_PGP="/tmp/pinsecret.gpg"
ENV SO_PIN_SECRET="/tmp/sopinsecret"
ENV SO_PIN_SECRET_PGP="/tmp/sopinsecret.gpg"


# For PKCS#11 Proxy Services
ENV PKCS11_PROXY_PORT=5657
# ENV PKCS11_DAEMON_SOCKET="tcp://0.0.0.0:5657"
ENV PKCS11_DAEMON_SOCKET="tls://0.0.0.0:${PKCS11_PROXY_PORT}"
ENV PKCS11_PROXY_TLS_PSK_FILE="/root/TLS-PSK"

EXPOSE ${PKCS11_PROXY_PORT}

#  It's better to working with mount for token directorys
COPY softhsm2.conf /root/softhsm2.conf
COPY PIN_PRO.testing.public.asc ${PIN_PRO_PGP_PUBLICKEY}
COPY TLS-PSK ${PKCS11_PROXY_TLS_PSK_FILE}
COPY initialize.sh initialize.sh

# # Initialized the PIN Secret and SO-PIN Secret
# RUN openssl rand -hex 32 > ${PIN_SECRET} && \
#     openssl rand -hex 32 > ${SO_PIN_SECRET}


# RUN gpg --import ${PIN_PRO_PGP_PUBLICKEY} && \
#     gpg -e -u 'SoftHSMv2_ADMIN' --trust-model always -r ${PGP_RECIPIENT} ${PIN_SECRET}  && \
#     gpg -e -u 'SoftHSMv2_ADMIN' --trust-model always -r ${PGP_RECIPIENT} ${SO_PIN_SECRET}

# Change To USTC Mirror For China Users
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

# # Dependencies
# RUN apt-get update && apt-get -y install git\
#     autoconf automake pkg-config botan openssl llvm curl gcc sqlite3 \
#     libcrypto++ libsqlite3-dev libp11-dev libbotan-2-dev libengine-pkcs11-openssl libtool libssl-dev zlib1g-dev

# RUN git clone https://github.com/opendnssec/SoftHSMv2

RUN apt-get update && apt-get install -y softhsm2 opensc opensc-pkcs11 \
    ca-certificates \
    git-core \
    build-essential \
    cmake \
    libssl-dev \
    libseccomp-dev \
    tzdata

RUN git clone https://github.com/SUNET/pkcs11-proxy && \
    cd pkcs11-proxy && \
    cmake . && \
    make && \
    make install

RUN chmod a+x initialize.sh
ENTRYPOINT [ "bash","./initialize.sh" ]


# CMD softhsm2-util --init-token --slot 0 --label ${TOKENLABLE} --pin 1234 --so-pin 1234 && \
#     /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so


# CMD softhsm2-util --init-token --slot 0 --label ${TOKENLABLE} --pin ${SECRET} --so-pin ${SECRET} && \
#     /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so

# CMD nohup sh -c /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so &

