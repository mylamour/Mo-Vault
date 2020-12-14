import os
import datetime
from subprocess import Popen, PIPE

from cryptography import x509

from cryptography.hazmat.primitives import hashes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.backends.openssl import backend

# from src import HSM, Svault, int_to_bytes, hex_to_bytes
# from pkcs11 import KeyType, ObjectClass, Mechanism
# from pkcs11.exceptions import PinIncorrect, NoSuchKey, NoSuchToken, MultipleObjectsReturned


# # engine.engine_load_private_key(e, alias)

# pki = HSM(slot="sofunny", pin="test")
# pki_pub, pki_priv = pki.get_rsa("SSL Issue CA 01", secret_version=2)


key_file_path = "tests/key.pem"
csr_file_path = "tests/csr.pem"
ca_certs = "certs/spki.cert.pem"
newcert_file_path = "tests/cert.pem"
p12file="newcerts/test.p12"

key_pass = b"pass"
key_id = "696976398:02"

# COUNTRY_NAME
# STATE_OR_PROVINCE_NAME
# LOCALITY_NAME
# ORGANIZATION_NAME
# COMMON_NAME

DOMINAS = ["www.example.com", "localhost", "127.0.0.1"]
SANAMES = [x509.DNSName(i) for i in DOMINAS]


key = rsa.generate_private_key(
    public_exponent=65537, key_size=2048, backend=backend)


#  generate private key
# with open(key_file_path, "wb") as f:
#     f.write(key.private_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PrivateFormat.TraditionalOpenSSL,
#         encryption_algorithm=serialization.BestAvailableEncryption(key_pass)
#     ))


# generate csr


subject = issuer = x509.Name([
    # Provide various details about who we are.
    x509.NameAttribute(NameOID.COUNTRY_NAME, u"CN"),
    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"JS"),
    x509.NameAttribute(NameOID.LOCALITY_NAME, u"SZ"),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"PP"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
])

csr = x509.CertificateSigningRequestBuilder().subject_name(subject).add_extension(
    x509.SubjectAlternativeName(SANAMES),
    critical=False,
    # Sign the CSR with our private key.
).sign(key, hashes.SHA256(), backend=backend)

with open(csr_file_path, "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))

p = Popen(["openssl x509 -req -engine pkcs11 -in {} -CAkeyform engine -CAkey {} -CA {}  -days 365 -sha256 -out {}".format(
    csr_file_path, key_id, ca_certs, newcert_file_path)],  stdin=PIPE, stdout=PIPE, stderr=PIPE, shell=True )


if os.path.exists(p12file) and os.path.isfile(p12file):
    with open(p12file, "wb") as f:
        f.write(key,)


# from cryptography.hazmat.primitives.serialization import load_pem_private_key
# key = load_pem_private_key(open("tests/key.pem").read().encode("utf-8"), password=b"pass", backend=backend)
# cert = x509.load_pem_x509_certificate(open(newcert_file_path).read().encode("utf-8"), backend)

#  How to use pkcs11 private key to sign it?
#  Todo, new backend with pkcs11 ? backend with conf file? load engine? or private key sign file with x509 format? oscp ?
# csr = x509.load_pem_x509_csr(open("pkitests/csr2.pem").read().encode("utf-8"), backend=default_backend())


# # Sign a cert
# cert = x509.CertificateBuilder().subject_name(subject).issuer_name(issuer).public_key(key.public_key()).serial_number(x509.random_serial_number()
#  ).not_valid_before(
#      datetime.datetime.utcnow()
#  ).not_valid_after(
#      # Our certificate will be valid for 10 days
#      datetime.datetime.utcnow() + datetime.timedelta(days=10)
#  ).add_extension(
#      x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
#      critical=False,
#  # Sign our certificate with our private key
#  ).sign(key, hashes.SHA256(),backend=backend)


# with open("pkitests/certificate.pem", "wb") as f:
#      f.write(cert.public_bytes(serialization.Encoding.PEM))
