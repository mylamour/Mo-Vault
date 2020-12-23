#!/bin/bash

# nohup python3 /root/app.py && 

# Init New Slot

# Init Dropzone HSM Key
# curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"dropzone/rsa", "secret_version":"1"}'  http://mo.vault.eaas:8443/gen/key/rsa
curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"dropzone/rsa", "secret_version":"1"}' http://mo.vault.eaas:8443/gen/key/rsa
# pkcs11-tool --module /usr/local/lib/softhsm/libsofthsm2.so -l --keypairgen --key-type rsa:4096 --id 1 --label "dropzone/rsa"
cd /dropzone/ && mkdir -p keks remote/s && python3 dropzone.py <<< test