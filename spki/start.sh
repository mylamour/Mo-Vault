#!/bin/bash

export PIN=$(openssl rand -hex 4)

softhsm2-util --init-token --slot 0 --label spki --so-pin $PIN --pin $PIN  > slot.log

SLOTID=$(awk -F " " '{print $11}' slot.log)

# echo -e "init = $SLOTID \npin = $PIN" > /tmp/changeit
echo -e "PIN = $PIN \ninit = $SLOTID" > /tmp/changeit
sed -i '/changemyslotandpin/ r /tmp/changeit' /etc/ssl/openssl.cnf


pkcs11-tool --module /usr/local/lib/softhsm/libsofthsm2.so -l --keypairgen --key-type rsa:4096 --id 01 --label "SSL Root CA 01" --token-label spki <<< $PIN
pkcs11-tool --module /usr/local/lib/softhsm/libsofthsm2.so -l --keypairgen --key-type rsa:2048 --id 02 --label "SSL Issue CA 01" --token-label spki <<< $PIN

export rootcakeyid=$(echo $(awk -F " " '{print $11}' slot.log):01)
export issuecakeyid=$(echo $(awk -F " " '{print $11}' slot.log):02)

cat /tmp/changeit

mkdir -p /spki/ca/certs /spki/ca/newcerts /spki/ca/crl /spki/ca/csr /spki/ca/crl/private
mkdir -p /spki/ca/intermediate/certs /spki/ca/intermediate/newcerts /spki/ca/intermediate/csr /spki/ca/intermediate/crl /spki/ca/intermediate/private
chmod 700 /spki/ca/crl/private /spki/ca/intermediate/private

touch /spki/ca/index.txt /spki/ca/intermediate/index.txt
echo 1000 > /spki/ca/serial 
echo 1000 > /spki/ca/intermediate/serial
echo 1000 > /spki/ca/intermediate/crlnumber
echo 1000 > /spki/ca/certs/spki.cert.srl

# openssl req -config openssl.cnf

# create root ca

cd /spki/ca
openssl req -new -x509 -days 7300 -sha512 -extensions v3_ca -engine pkcs11 -keyform engine -key $rootcakeyid  -out certs/root.ca.cert.pem -subj "/C=CN/ST=JS/L=SZ/O=PayPal/OU=GoPay/CN=SPKI SSL ROOT CA 01"

#create issue ca
## generate issue ca csr
cd /spki/ca/intermediate/
cp /spki/ca/certs/root.ca.cert.pem /spki/ca/intermediate/certs/

openssl req -engine pkcs11 -keyform engine -key $issuecakeyid -new -sha512  -out /spki/ca/intermediate/csr/issue.ca.csr -subj "/C=CN/ST=JS/L=SZ/O=PayPal/OU=GoPay/CN=SPKI SSL ISSUE CA 01"
## sign csr by root ca
# use -batch to escape the prompt
openssl ca -batch -engine pkcs11 -keyform engine -keyfile $rootcakeyid -extensions v3_intermediate_ca -days 3650 -notext -md sha512 -in csr/issue.ca.csr -out /spki/ca/intermediate/certs/issue.ca.cert.pem 

cat /spki/ca/intermediate/certs/issue.ca.cert.pem /spki/ca/certs/root.ca.cert.pem > /spki/ca/spki.cert.pem 

if [ -f /spki/ca/spki.cert.pem ]; then
    openssl x509 -in /spki/ca/spki.cert.pem -noout -text
fi

mkdir -p /spki/softhsm/
cp -r /var/lib/softhsm/tokens/ /spki/softhsm/