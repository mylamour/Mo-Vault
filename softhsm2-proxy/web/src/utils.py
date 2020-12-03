# In [87]: oneapp_aes_test[Attribute.VALUE]
# Out[87]: b'\x9b\n\xf1M1{&\xd2z\xa2\x99\xef\xc7c*\xba'

# In [88]: oneapp_aes_test[Attribute.VALUE].hex()
# Out[88]: '9b0af14d317b26d27aa299efc7632aba'

# In [89]: bytes.fromhex(oneapp_aes_test[Attribute.VALUE].hex())
# Out[89]: b'\x9b\n\xf1M1{&\xd2z\xa2\x99\xef\xc7c*\xba'
from collections import defaultdict

def bytes_to_hex(binary_data: bytes) -> hex:
    return binary_data.hex()


def hex_to_bytes(hex_data: hex) -> bytes:
    return bytes.fromhex(hex_data)


def int_to_bytes(number: int) -> bytes:
    return number.to_bytes(length=(8 + (number + (number < 0)).bit_length()) // 8, byteorder='big', signed=True)

def bytes_to_int(binary_data: bytes) -> int:
    return int.from_bytes(binary_data, byteorder='big', signed=True)


def string_to_bytes(str_data: str) -> bytes:
    return str_data.encode('utf-8')


def bytes_to_string(binary_data: bytes) -> str:
    return binary_data.decode("utf-8")

def tree(): return defaultdict(tree)



# def bin2hex(binStr):
#     return binascii.hexlify(binStr)

# def hex2bin(hexStr):
#     return binascii.unhexlify(hexStr)