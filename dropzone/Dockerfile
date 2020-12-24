FROM python:3.8
LABEL maintainer "Mour <mylamour@163.com>"
# for prod it's better to use python:3.8
# dor debug it's better to use mo-vault:base

ARG DROPZONE_PORT
ARG DROPZONE_SECRET_PATH
ARG DROPZONE_SECRET_VERSION

ENV DROPZONE_PORT=$DROPZONE_PORT
ENV DROPZONE_SECRET_PATH=$DROPZONE_SECRET_PATH
ENV DROPZONE_SECRET_VERSION=$DROPZONE_SECRET_VERSION

ENV EAAS_URL="http://mo.vault.eaas:8443"

COPY ./* /dropzone/
RUN mkdir /dropzone/keks && pip3 install -r /dropzone/requirements.txt
ENTRYPOINT [ "bash","/dropzone/dropzone.sh" ]