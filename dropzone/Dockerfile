FROM mo-vault:base
LABEL maintainer "Mour <mylamour@163.com>"


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