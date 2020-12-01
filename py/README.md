

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
ian@star01:~/Desktop/Mo-softhsm$ curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"random_test/rsa", "secret_version":"2","plaintext":"you are handsome man" }' http://127.0.0.1:8080/key/encrypt/rsa
{
  "ciphertext": "a92b38d38140bd2dcb6651ee0a7001af7e48506fdecf2b30ad5767bd229456be1a5b60d8095ac3702dfd34ee4bbd46c35449ad006a48bd185e4090cfd683da26cb0e18b4c35e0a0bd0e8f11659fed5c95a120b6b9ea970b480b59cbfcd2a1f1805a652a6e31df9377456253e106656086026c54b0c81460d2990726a612a8511d755db4919bae1a3fe78e2850073f53e81b9b2cb12f16cfbc890dce2e47a3e47f9e0da4c03f337f94d5dad12b5e70cc89458730c57fece59f737a2e6fdc6713571bdcbf0178746fa595aba520f7e9050be8b20bc7ae606d96bbeeedd4039d86f0899e0ac5aa60040c5a527e23a788fcf3cda70c70e6b7043e8beec4d85c297b5"
}

ian@star01:~/Desktop/Mo-softhsm$ curl --header "Content-Type: application/json"  --request POST --data '{"secret_path":"random_test/rsa","secret_version":"2", "ciphertext":"593834fa8daa9a0ae9f87f40554318ed652540e4c73ad4e07bce7c4815daee468e79cb365bcff4284762bd330eedcd0ba2b4f107c30c9f391a95a594072b2bc11e8706cff3d690f1e1cfcd146750ab4d6239991ac2aa1f87367ed903385d3a21bb8fd5de333f84efa5468e45a503bf4a3e813b7704486141a0755d11b1afdb97eebdb5ac35a6301fc773a4c9445287dadeadac416a3cdb6cfd9de7262e6e64ff201a27ef7cf4675171de42e8f4dedc75a276a26515a490ad1709a2f7dae0a5767c18c6f887db0748dbb67dcab2aeb206fe3946edca083f6198c7c1794a48e1c00fb9ad9dd6d98b4cb97569205936fce4978f581d16a1d116a4875aadbaeecafc"}' http://127.0.0.1:8080/key/decrypt/rsa
{
  "plaintext": "you are handsome man"
}


```