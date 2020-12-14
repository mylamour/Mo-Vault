
```bash
openssl x509 -req -engine pkcs11 -in tests/csr.pem -CAkeyform engine -CAkey 696976398:02 -CA certs/spki.cert.pem  -days 365 -sha256 -out newcerts/localhost.cert.pem 
```

also you can configure `PIN=pass` in openssl config file
