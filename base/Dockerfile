FROM ubuntu:latest
LABEL maintainer "Mour <mylamour@163.com>"

ENV LANG=en_US.UTF-8
ENV DEBIAN_FRONTEND=noninteractive

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