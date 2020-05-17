import binascii
from binaryornot.check import is_binary
import os

print(len("hello"))
s = '5\x00\x00'
print(len(s))
print(s.find('\x00'))

'''
# Open in binary mode (so you don't read two byte line endings on Windows as one byte)
# and use with statement (always do this to avoid leaked file descriptors, unflushed files)
with open('output', 'rb') as f:
    # Slurp the whole file and efficiently convert it to hex all at once
    hexdata = binascii.hexlify(f.read())
    print(hexdata)

print(is_binary('output'))

with open('output', 'rb') as file:
    fileContent = file.read()
print(fileContent)
with open('test.txt', 'rb') as file:
    fileContent = file.read()
print(fileContent)
print(os.path.getsize('testlarge.txt'))

buffer = "hello"
missing = 20 - buffer.sizeof()
buffer += []
'''