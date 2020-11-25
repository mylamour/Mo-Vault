

<p align="center">
  <img src="https://user-images.githubusercontent.com/12653147/99629727-75269300-2a73-11eb-8dce-16550c9ee1ce.png"  width=345/>
</p>



# Intro

This is a basic usage for `SoftHsm2` and `pkcs11-proxy`. now we are building a env with docker file. it mainly included four part.
1. Basic Env, also `SoftHsm2` and `pkcs11-proxy` 
2. Upload PGP Public Key when you try to building this image, it was designed for protected the `pin` vaule and `so-pin` vaule
3. Initilized the `slot` with random `32 bit hex` vaule and encrypt the vaule with `PGP Public Key`
4. Enable `pkcs11-proxy`


# How to use

1. Genreate PGP key with `gpg --full-generate-key` and export the public with `gpg --export xxxx > PIN_PRO.testing.public.asc` to `softhsm2-proxy/publickeys` folder.   make sure the numbers of gpg keys should equal with config file `.env.dev`. field: `HSM_KEYSHARES`

2. Generate a randome string for `TLS-PSK`,  You can use the following command to do that `echo -e $(openssl rand -hex 32):$(openssl rand -hex 32) > TLS-PSK`

3. Build the image with `docker-compose --env-file ./config/.env.dev build`, You can change the configuration in `./config/.env.dev`

4. Run the container `docker run --rm -v $PWD/tokens/user02:/var/tokens -p 5657:5657 mo-softhsm2-proxy:latest`

Notices:
>  Please keep use absolute path when we try to mount the `volum`

Now, you will able to use `softhsm2` with `pkcs11-proxy`, and `pkcs11-proxy` was listening on `0.0.0.0:5657` with `TLS` supported

# How to testing

After we start the container with `docker run --rm -it -v $PWD/tokens/user01:/var/tokens mylamour/more-softhsm2-proxy`, you will see the `gpg` file was placed in `$PWD/tokens/user01`, you will get the slot token after working with `gpg -d pinsecret.gpg`, in this repo, the testing key's password was `test`. it's weakness, **you must setting a strong password for prod env.**

Get token from gpg files 
```bash
find . -type f -name "*.pin.gpg" -exec gpg -d {} \; > /tmp/tokens | secret-share-combine 
```

![image](https://user-images.githubusercontent.com/12653147/100181707-da680180-2f15-11eb-8978-fd768375360f.png)


you can find more details about `secret-share-combine` and `secret-share-split` in `softhsm2-proxy/sss/readme.md`
This is just for test purpose. you should get the shares from each `Key Custodian` , and make sure it was only stored in memory.

as you can see in this picture, i was login into container and use below commands to have a testing:
```bash
root@803b461774cd:/# export PKCS11_PROXY_SOCKET="tls://172.17.0.2:5657"
root@803b461774cd:/# pkcs11-tool --module=/usr/local/lib/libpkcs11-proxy.so -L
Available slots:
Slot 0 (0x9a12019): SoftHSM slot ID 0x9a12019
  token label        : DEMO
  token manufacturer : SoftHSM project
  token model        : SoftHSM v2
  token flags        : login required, rng, token initialized, PIN initialized, other flags=0x20
  hardware version   : 2.5
  firmware version   : 2.5
  serial num         : 0b1650b589a12019
  pin min/max        : 4/255
Slot 1 (0x1): SoftHSM slot ID 0x1
  token state:   uninitialized
root@803b461774cd:/# pkcs11-tool --module=/usr/local/lib/libpkcs11-proxy.so -O -l
Using slot 0 with a present token (0x9a12019)
Logging in to "DEMO".
Please enter User PIN:
```

Notices:
> If you connect the softhsm-proxy from another server, please make sure you installed the `libpkca11-proxy.so` and export the TLS PSK file to env. eg. `export PKCS11_PROXY_SOCKET="tls://172.17.0.2:5657"`

![image](https://user-images.githubusercontent.com/12653147/99552255-c1cc8880-29f7-11eb-8bb3-d44c88926be8.png)



# Notices

1. exec the pkcs11-proxy in background
`nohup sh -c /usr/local/bin/pkcs11-daemon /usr/lib/softhsm/libsofthsm2.so &`
2. gpg encrypt file without interative.
    `gpg -e -u 'SoftHSMv2_ADMIN' --trust-model always -r PGP_RECIPIENT PIN_SECRET`
3. if softhsm2 was build manuly, you should change the lib path.
4. slot token label was able to changed with `docker run -e TOKENLABLE=""` also you can modified the `Dockerfile`
5. mount voulme,  `- ${PWD}/secrets/:/secrets` is not working, `- ${PWD}/secrets:/secrets` is working
6. docker rm none tags image `docker rmi $(docker images --filter "dangling=true" -q --no-trunc)`
7. list user's public keys `gpg --list-public-keys --batch --with-colons | grep pub | cut -d: -f5`

# Resources
* [Pass variable from docker-compose file to docker file](https://github.com/docker/compose/issues/5600)
