import aess
from time import time

key = str(time())
print("Key:", key)
msg = "Chirag"
m2 = "Chirag"
print(type(msg))
ct = aess.encrypt(msg, key)
ct2 = aess.encrypt(m2, key)

if ct == ct2:
    print("Same CT")
print("Cipher text:", ct)


pt = aess.decrypt(ct, key)

print("Deciphered Text:", pt)


