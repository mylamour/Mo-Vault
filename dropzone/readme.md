![dropzone](https://user-images.githubusercontent.com/12653147/101760437-d0e5b880-3b15-11eb-9101-af7bfc5f6b03.gif)


* use lftp  with ssl 

```bash

ian@star01:~/Desktop$ lftp
lftp :~> set ftp:ssl-force true
lftp :~> connect 127.0.0.1:2121
lftp 127.0.0.1:~> login s
Password: 
lftp s@127.0.0.1:~> ls
ls: Fatal error: Certificate verification: Not trusted (7D:FA:4B:08:60:6E:86:B8:44:E9:2D:8B:BE:50:1D:5C:63:32:F3:84)
lftp s@127.0.0.1:~> set ssl:verify-certificate no
lftp s@127.0.0.1:~> ls
drwxrwxr-x   2 ian      ian          4096 Dec 10 08:03 openssl

```


* generate ssl cert
` openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365`
 
 * upload mutliple file without prompt
```bash
ftp > prompt
interactive mode off
ftp > mput *
```
