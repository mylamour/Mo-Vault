#!/bin/bash

# Initialized the PIN Secret and SO-PIN Secret
openssl rand -hex 32 > ${PIN_SECRET} && openssl rand -hex 32 > ${SO_PIN_SECRET}

export PINSECRET=$(cat ${PIN_SECRET})
export SOPINSECRET=$(cat ${SO_PIN_SECRET})
export PINSHARES="/tmp/pinshares.txt"
export SOPINSHARES="/tmp/sopinshares.txt"

if [ ${HSM_KEYSHARES}  -le ${HSM_KEY_THESHOLD} ]
then
     echo "Please check your config file and make sure HSM_KEY_THSHOLD<=HSM_KEYSHARES"
     exit
fi


# import pgp keys
for publickey in $(ls $PWD/${PIN_PRO_PGP_PUBLICKEYS_DIR}/*)
do
    echo "[Processing] Import $publickey"
    gpg --import $publickey

done

# split token to each part and output to file
echo $PINSECRET | ${SSS_SPLIT} -n ${HSM_KEYSHARES} -t ${HSM_KEY_THESHOLD} > ${PINSHARES}
echo $SOPINSECRET | ${SSS_SPLIT} -n ${HSM_KEYSHARES} -t ${HSM_KEY_THESHOLD} > ${SOPINSHARES}

# split file with suffix
split -l 1 ${PINSHARES} pinshares_
split -l 1 ${SOPINSHARES} sopinshares_


# KEYIDS=$(gpg --list-public-keys --batch --with-colons | cut -d: -f5 | grep -v '^$' )
# KEYIDS=$(gpg --list-public-keys --batch --with-colons | grep uid |  cut -d: -f8)
KEYIDS=$(gpg --list-public-keys --batch --with-colons | grep pub | cut -d: -f5)

echo $KEYIDS
COUNTER=0

# bash was able to use (()) array
pinfiles=( $( ls pinshares_* ) )
sopinfiles=( $( ls sopinshares_* ) )

echo ${pinfiles[$COUNTER]}

# get each file and encrypt it with pgp public key
for recipient_id in $KEYIDS
do
    echo "[Processing $COUNTER] Encryption Recipient Id: $recipient_id"

    echo "Processing......" ${pinfiles[$COUNTER]} ${sopinfiles[$COUNTER]}
    gpg -e -u "SoftHSMv2_ADMIN" --trust-model always -r $recipient_id ${pinfiles[$COUNTER]}
    find . -type f -name "pinshares_*.gpg" -print 2>/dev/null -exec mv {} $recipient_id.pin.gpg \;

    gpg -e -u "SoftHSMv2_ADMIN" --trust-model always -r $recipient_id ${sopinfiles[$COUNTER]}
    find . -type f -name "sopinshares_*.gpg" -print 2>/dev/null -exec mv {} $recipient_id.sopin.gpg \;
    
    COUNTER=$[$COUNTER +1]

done


softhsm2-util --init-token --slot 0 --label ${TOKENLABEL} --pin ${PINSECRET} --so-pin ${SOPINSECRET}

# unset PINSECRET
# unset SOPINSECRET

find . -type f -name "*pin.gpg" -print 2>/dev/null -exec mv {} /var/tokens \;

rm -rf ${PIN_SECRET} ${SO_PIN_SECRET} ${PINSHARES} ${SOPINSHARES}
rm -rf pinshares_* sopinshares_*

nohup /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so  > /dev/null &

# export FLASK_APP=/root/web/app.py && cd /root/web && flask run
# export FLASK_APP=/root/app.py && flask run

cd /root/ && python3 /root/app.py