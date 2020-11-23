from shamirss import SecretSharer


shares = SecretSharer.split_secret("c4bbcb1fbec99d65bf59d85c8cb62ee2db963f0fe106f483d9afa73bd4e39a8a", 2, 3)


print(shares)

print(SecretSharer.recover_secret(shares[0:2]))

print(SecretSharer.recover_secret(shares[1:]))

from shamirss import PlaintextToHexSecretSharer

shares = PlaintextToHexSecretSharer.split_secret("correct horse battery staple", 2, 3)
print( PlaintextToHexSecretSharer.recover_secret(shares[0:2]))