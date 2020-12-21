#!/bin/bash

# nohup python3 /root/app.py && 

# Init Dropzone HSM Key

# curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"${DROPZONE_SECRET_PATH}", "secret_version":"${DROPZONE_SECRET_VERSION}}"}' ${EAAS_HOST}

cd /dropzone/ && mkdir -p keks remote/s && python3 dropzone.py <<< test