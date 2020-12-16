FROM ubuntu:latest
LABEL maintainer "Mour <mylamour@163.com>"

ENV LANG=en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

# Change To USTC Mirror For China Users
RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y opensc opensc-pkcs11 \
    ca-certificates \
    git-core \
    build-essential \
    tzdata \
    python3 \
    python3-pip \
    autoconf automake pkg-config botan openssl llvm curl gcc cmake sqlite3 \
    libtool libcrypto++ libseccomp-dev libssl-dev libsqlite3-dev libp11-dev libbotan-2-dev libengine-pkcs11-openssl  zlib1g-dev

# complied manually with botan as crypto backend ,and enable sqlite support
RUN git clone https://github.com/opendnssec/SoftHSMv2 && \
    cd SoftHSMv2 && \
    ./autogen.sh && \
    ./configure --with-objectstore-backend-db --with-crypto-backend=botan && \
    make -j8 && make install 

RUN git clone https://github.com/SUNET/pkcs11-proxy && \
    cd pkcs11-proxy && \
    cmake . && \
    make && \
    make install