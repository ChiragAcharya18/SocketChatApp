from Crypto.Cipher import AES
from Crypto.Hash import MD5


def hashing(key):
    hash_obj = MD5.new(key.encode('utf-8'))
    hkey = hash_obj.digest()
    return hkey


def encrypt(info, key):
    msg = info
    hkey = hashing(key)
    BLOCK_SIZE = 16
    PAD = "#"
    padding = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PAD
    cipher = AES.new(hkey, AES.MODE_ECB)
    result = cipher.encrypt(padding(msg).encode('utf-8'))
    return result


def decrypt(info, key):
    msg = info
    PAD = "#"
    hkey = hashing(key)
    decipher = AES.new(hkey, AES.MODE_ECB)
    pt = decipher.decrypt(msg).decode('utf-8')
    pad_index = pt.find(PAD)
    result = pt[:pad_index]
    return result
