import sqlite3
from sqlite3 import Error
from zxcvbn import zxcvbn
import math
import hashlib
import pyAesCrypt
import io

#5aff4a05f7bd202fab6037e7e7ab3758fb139452b61ac63ff2dbcf8db24b819f7905c4f5fa0430f9ca15a1e6ab534eefa99b79663da866a5ac49522543e62559

path = '/home/rex/PycharmProjects/Armour/Database.db'

# # Read & binary mode
# with open(path, 'rb') as opened_file:
#     content = opened_file.read()
#     print("Plaintext" + str(content))
#     sha512 = hashlib.sha512()
#     sha512.update(content)
#     print('SHA512:{}'.format(sha512.hexdigest()))
#     opened_file.close()

bufferSize = 64 * 1024
password = "please-use-a-long-and-random-password"

# Encrypting file.
# with open(path, 'rb') as opened_file:
#     content = opened_file.read()
#     # binary data to be encrypted
#     pbdata = content
#     # input plaintext binary stream
#     fIn = io.BytesIO(pbdata)
#     # initialize ciphertext binary stream
#     fCiph = io.BytesIO()
#     # encrypt stream
#     pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)
#     # print encrypted data
#     print("This is the ciphertext:\n" + str(fCiph.getvalue()))
#     opened_file.close()
#
# # Writing encryption
# with open(path, 'wb') as opened_file:
#     opened_file.write(fCiph.getvalue())
#     opened_file.close()

with open(path, 'rb') as opened_file:
    fCiph = io.BytesIO(opened_file.read())
    # initialize decrypted binary stream
    fDec = io.BytesIO()
    # get ciphertext length
    ctlen = len(fCiph.getvalue())
    # go back to the start of the ciphertext stream
    fCiph.seek(0)
    # decrypt stream
    pyAesCrypt.decryptStream(fCiph, fDec, password, bufferSize, ctlen)
    # print decrypted data
    print("Decrypted data:\n" + str(fDec.getvalue()))

# Writing encryption
with open(path, 'wb') as opened_file:
    opened_file.write(fDec.getvalue())
    opened_file.close()



# results = zxcvbn('JohnSmith123')
#
# print(math.log2(results["guesses"]))
