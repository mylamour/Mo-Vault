#!/bin/bash

# Init New Slot
#pass
# Init Dropzone HSM Key
while true; do

  curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"dropzone/rsa", "secret_version":"1"}' http://mo.vault.eaas:8443/gen/key/rsa > log.info

  if grep -q "Key was exsits" log.info; then
       break
  fi
  sleep 3
done

useradd s
useradd demo

cd /dropzone/ && python3 dropzone.py <<< test
