FROM mo-vault:base
LABEL maintainer "Mour <mylamour@163.com>"

COPY conf/openssl.cnf /etc/ssl/openssl.cnf
COPY conf/ssl.openssl.cnf /usr/lib/ssl/openssl.cnf

COPY start.sh /root/start.sh
COPY spki.py /root/spki.py


ENTRYPOINT [ "bash", "/root/start.sh" ]