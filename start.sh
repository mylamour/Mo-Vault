#!/bin/sh

echo -e $(openssl rand -hex 32):$(openssl rand -hex 32) > TLS-PSK

docker build . -t testshsm

docker run --rm -it -v $PWD/tokens:/var/tokens testshsm