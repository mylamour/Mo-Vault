

![image](https://user-images.githubusercontent.com/12653147/100613207-1ef90000-334f-11eb-8f70-9d90c32d0d47.png)


```bash
ian@star01:~/Desktop/Mo-softhsm$ curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"random_test/rsa", "secret_version":"1"}' http://127.0.0.1:8080/gen/key/rsa
{
  "Info": "RSA Key with random_test/rsa Generated"
}
ian@star01:~/Desktop/Mo-softhsm$ curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"random_test/rsa", "secret_version":"1"}' http://127.0.0.1:8080/gen/key/rsa
{
  "Info": "Key was exsits"
}
ian@star01:~/Desktop/Mo-softhsm$ curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"random_test/rsa", "secret_version":"1","plaintext":"you are handsome man" }' http://127.0.0.1:8080/key/encrypt/rsa
{
  "ciphertext": "(None, '55f71d38a83537994cac2f6b0cc3c3756897f44799599059b1edb6a0d8e41234f59ad11c203d1a0645fe59fb01c7bfca89c8f0241c02c91031d7be66e2a016b7c195b600dd78b356af2e1c949700ffe8550cb7766efd7c7cffc941e201a3fa8131a33f42b9aba1f0b32272cbee202ac52ae65d403987aa62a8ea5fcef97626f49fdf8acbdce80d891ec4a2413d63306945be575e4b7f138ac551c73a70c1bee045092123fbeed006491403dff231a9a2a5ed01d2aadae86cee0d796dab51ba7baca94912a33d3a648ab8624763c2abfb1cbdc702e6ae80a26107ffb18fe8d4d11979711ad93e0be1a431a8d679c7a4878c27827e27fbffa170a2a8bb3bdcbd84')"
}


```