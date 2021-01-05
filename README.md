# Intro

There was some folder

* Base (Base Image which contained softhsm2 & pkcs11 relevant package)
* Dropzone (A simple FTP Server with Data-At-Rest-Encryption)
* Spki (A PKI System with Openssl & Softhsm2)
* Softhsm2-proxy (A Simple Encryption As a Services)

# QuickStart

put `3` public pgp key into `softhsm2-proxy/publickeys` folder, those keys was used to encrypt slot's `PIN`

```bash
docker-compose  --env-file ./config/.env.dev build
docker-compose  --env-file ./config/.env.dev up
```

each time when you want genreate a new one token , you can just `rm -rf local/tokens/user02 local/remote local/keks`. And for the details, you just need to enter each folder and check the `reademe` file