import binascii
from binaryornot.check import is_binary
# Open in binary mode (so you don't read two byte line endings on Windows as one byte)
# and use with statement (always do this to avoid leaked file descriptors, unflushed files)
with open('test.txt', 'rb') as f:
    # Slurp the whole file and efficiently convert it to hex all at once
    hexdata = binascii.hexlify(f.read())
    print(hexdata)

print(is_binary('/Users/aidenw/Desktop/Malware/Trailmalware/Trailmalware/reverseshell'))

with open('/Users/aidenw/Desktop/Malware/Trailmalware/Trailmalware/reverseshell', 'rb') as file:
    fileContent = file.read()
print(fileContent)