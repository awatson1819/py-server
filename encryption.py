import secrets

from Crypto.Cipher import AES


num = secrets.token_bytes(32)
iv = secrets.token_bytes(16)
print(num)
print(iv)
file = open("key.key", "wb")
file.write(num)
aes = AES.new(num, AES.MODE_CBC, iv)
data = 'hello world 1234' # <- 16 bytes
encd = aes.encrypt(data)

print("encrypted = ", encd)

aes = AES.new(num, AES.MODE_CBC, iv)
decd = aes.decrypt(encd)
print("decryped = ", decd)
