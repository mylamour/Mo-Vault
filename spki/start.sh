#!/bin/bash

export PIN=$(openssl rand -hex 4)

softhsm2-util --init-token --slot 0 --label spki --so-pin $PIN --pin $PIN  > slot.log

SLOTID=$(awk -F " " '{print $11}' slot.log)

echo -e "init = $SLOTID \npin = $PIN" > /tmp/changeit
sed -i '/changemyslotandpin/ r /tmp/changeit' /etc/ssl/openssl.cnf


pkcs11-tool --module /usr/local/lib/softhsm/libsofthsm2.so -l --keypairgen --key-type rsa:4096 --id 01 --label "SSL Root CA 01" --token-label spki <<< $PIN
pkcs11-tool --module /usr/local/lib/softhsm/libsofthsm2.so -l --keypairgen --key-type rsa:2048 --id 02 --label "SSL Issue CA 01" --token-label spki <<< $PIN

set rootcakeyid=$(echo $(awk -F " " '{print $11}' slot.log):01)
set issuecakeyid=$(echo $(awk -F " " '{print $11}' slot.log):02)

cat /tmp/changeit

mkdir -p /spki/certs /spki/csr
touch /spki/index.txt
echo 1000 > /spki/serial
echo 1000 > /spki/certs/spki.cert.srl

# create root ca
openssl req -new -x509 -days 7300 -sha512 -extensions v3_ca -engine pkcs11 -keyform engine -key $rootcakeyid -out /spki/certs/root.ca.cert.pem
#create issue ca
## generate issue ca csr
openssl req -engine pkcs11 -keyform engine -key $issuecakeyid -new -sha512  -out /spki/csr/issue.ca.csr
## sign csr by root ca
openssl ca -engine pkcs11 -keyform engine -keyfile $rootcakeyid -extensions v3_intermediate_ca -days 3650 -notext -md sha512 -in /spki/csr/issue.ca.csr -out /spki/certs/issue.ca.cert.pem 

cat /spki/certs/issue.ca.cert.pem /spki/certs/root.ca.cert.pem > /spki/certs/spki.cert.pem 

bash