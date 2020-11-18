#!/bin/bash


# Initialized the PIN Secret and SO-PIN Secret
openssl rand -hex 32 > ${PIN_SECRET} && openssl rand -hex 32 > ${SO_PIN_SECRET}

gpg --import ${PIN_PRO_PGP_PUBLICKEY} && \
gpg -e -u 'SoftHSMv2_ADMIN' --trust-model always -r ${PGP_RECIPIENT} ${PIN_SECRET}  && \
gpg -e -u 'SoftHSMv2_ADMIN' --trust-model always -r ${PGP_RECIPIENT} ${SO_PIN_SECRET}

export PINSECRET=$(cat ${PIN_SECRET})
export SOPINSECRET=$(cat ${SO_PIN_SECRET})

softhsm2-util --init-token --slot 0 --label ${TOKENLABLE} --pin ${PINSECRET} --so-pin ${SOPINSECRET}


rm -rf ${PIN_SECRET} ${SO_PIN_SECRET}
mv ${PIN_PRO_PGP_PUBLICKEY} ${PIN_SECRET_PGP} ${SO_PIN_SECRET_PGP} /var/tokens

/usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so
