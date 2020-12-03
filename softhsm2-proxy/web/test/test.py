import pytest
from src import HSM, Svault, int_to_bytes, hex_to_bytes
from pkcs11 import KeyType, ObjectClass, Mechanism
from pkcs11.exceptions import PinIncorrect, NoSuchKey, NoSuchToken, MultipleObjectsReturned


hsm = HSM(slot="OpenDNSSEC", pin="1234")



# def test_genaes():
#     # first time was True
#     # second time was False
#     t= hsm.gen_aes("app_aes/testa/funny",1)
#     assert t, True


# def test_genrsa():
#     t = hsm.gen_rsa("app_rsa/test/funny",1)
#     assert t, True

def test_getaes_multiple():
    with pytest.raises(MultipleObjectsReturned):
        hsm.get_aes("app_aes/testa/funny",1)

def test_getaes():
    assert hsm.get_aes("thisisrandomekey",2), hsm.SESSION.get_key(label="thisisrandomekey", id=int_to_bytes(2))

def test_aes_encrypt():
    aeskey = hsm.get_aes("thisisrandomekey",2)
    vault = Svault(aeskey)
    iv, ciphertext = vault.encrypt('thisistest')
    assert aeskey.encrypt('thisistest', mechanism_param=hex_to_bytes(iv)).hex(), ciphertext

def test_aes_decrypt():
    aeskey = hsm.get_aes("thisisrandomekey",2)
    vault = Svault(aeskey)
    iv, ciphertext = vault.encrypt('thisistest')
    assert aeskey.decrypt(ciphertext, mechanism_param=hex_to_bytes(iv)), "thisistest"

def test_getrsa_pub():
    pub, _ = hsm.get_rsa("app_rsa/test/funny",1)
    assert pub, hsm.SESSION.get_key(label="app_rsa/test/funny", id=int_to_bytes(1),key_type=KeyType.RSA, object_class=ObjectClass.PUBLIC_KEY)
    
def test_getrsa_priv():
    _, priv = hsm.get_rsa("app_rsa/test/funny",1)
    assert priv, hsm.SESSION.get_key(label="app_rsa/test/funny", id=int_to_bytes(1),key_type=KeyType.RSA, object_class=ObjectClass.PRIVATE_KEY)
    

def test_rsaencrypt():
    pub, _ = hsm.get_rsa("app_rsa/test/funny",1)
    pubV = Svault(pub)
    plaintext = "thisisatest"
    ciphertext = pubV.encrypt(plaintext)
    assert ciphertext, pub.encrypt(plaintext).hex()

def test_rsadecrypt():
    pub, priv = hsm.get_rsa("app_rsa/test/funny",1)
    pubV = Svault(pub)
    privV = Svault(priv)

    plaintext = "thisisatest"

    ciphertext = pubV.encrypt(plaintext)

    assert privV.decrypt(ciphertext), plaintext

def test_rsa_sign_verify():
    pub, priv = hsm.get_rsa("app_rsa/test/funny",1)
    pubV = Svault(pub)
    privV = Svault(priv)

    plaintext = "thisisatest"
    signature = privV.sign(plaintext)
    
    assert pubV.verify(plaintext, signature), True


