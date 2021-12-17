"""
ManyKeys.py v1.0.0 - Centralized Confidential Data Collection for Collaborative Online Studies
<https://github.com/adriansteffan/manykeys>

(c) Adrian Steffan <adrian.steffan [at] hotmail.de> <https://github.com/adriansteffan>
(c) Till Müller <https://github.com/TillMueller>
Licenced under GPLv3. See <https://raw.githubusercontent.com/adriansteffan/manykeys/main/LICENSE>
"""


from Crypto.Protocol.KDF import PBKDF2
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHAKE256, SHA256

import getpass

import base64
import sys
import os

OUTPUT_DIR_NAME = "decrypted"

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("The script will now prompt you to set a username and password.\n"
              "YOU MUST NOT LOSE THIS INFORMATION. Otherwise, you will not be able to recover your data. \n" 
              "Be sure to keep your password confidential.")
        input("Press Enter to continue...")

    username = input("Username: ")
    password = getpass.getpass("Password: ")

    # deterministically derive a RSA keypair from username and password
    # CSPRNG: implemented with SHAKE to support seeding
    seed = PBKDF2(password, username.encode('utf-8'), 16, count=1000000)
    private_key = RSA.generate(2048, randfunc=SHAKE256.new(seed).read)

    if len(sys.argv) == 1:
        data = private_key.public_key().export_key('PEM') + b';' + username.encode('utf-8')
        key_string = base64.urlsafe_b64encode(SHA256.new(data).digest() + data).decode('utf-8').rstrip("=")
        print(len(base64.urlsafe_b64encode(SHA256.new(data).digest() + data).decode('utf-8'))-len(key_string))

        with open("keystring.txt", 'w') as f:
            f.write(key_string)

        print("Your public keystring: \n" + key_string)

    else:
        output_dir = os.path.join(os.getcwd(), OUTPUT_DIR_NAME)

        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        for file in os.listdir(os.path.join(os.getcwd(), sys.argv[1])):
            if not file.endswith((".enc")):
                continue

            with open(file, "r") as f:
                enc_bytes = base64.b64decode(f.read())

            try:
                enc_session_key = enc_bytes[:256]
                nonce = enc_bytes[256:256+16]
                ciphertext = enc_bytes[256+16:-16]
                tag = enc_bytes[-16:]

                # Decrypt the session key with the private RSA key
                cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
                session_key = cipher_rsa.decrypt(enc_session_key)

                # Decrypt the data with the AES session key
                cipher_aes = AES.new(session_key, AES.MODE_GCM, nonce, mac_len=16, )
                data = cipher_aes.decrypt_and_verify(ciphertext, tag)

            except Exception:
                print("Could not decrypt file {}".format(file))
                continue


            with open(os.path.join(output_dir, file[:-4]), "wb") as f:
                f.write(data)
        print("Decrypting done.")


""" Unused code that implements decryption of the data via the python script
from Crypto import Random

# fix b64
padding = (4 - (len(key_string) % 4)) % 4
string = key_string + ("=" * padding)

data_all = base64.urlsafe_b64decode(string)
print(data_all)
checksum = data_all[:32]
data = data_all[32:]

if SHA256.new(data).digest() != checksum:
    print("")
    exit(1)

key, name = data.split(b';', 1)

with open("test.txt", 'rb') as f:
    plaintext = f.read()

session_key = Random.get_random_bytes(32)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(RSA.import_key(key.decode("utf-8")))
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_GCM)
ciphertext, tag = cipher_aes.encrypt_and_digest(plaintext)

with open("enc_test.txt", "wb") as f:
    [f.write(x) for x in (enc_session_key, cipher_aes.nonce, ciphertext, tag)]
"""
