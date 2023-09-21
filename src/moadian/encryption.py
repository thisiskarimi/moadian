import os
import base64
import subprocess
import sys
import json
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def xor_and_encrypt_data(data, key, iv):
    base_command = "php "+os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)
        ), "helper.php"
    )

    """
    We need to identify the platform on which the code is currently running 
    because there may be platform-specific issues with the code. 
    Depending on the platform, modifications may be necessary to ensure that the 
    code runs smoothly and without errors. 
    For example, if running on Windows, we may need to remove single quotations 
    and dump the data again.
    """
    if sys.platform == 'win32':
        base_command += " {key} {iv} {invoice} "
        data = json.dumps(data)
    else:
        base_command += " {key} {iv} '{invoice}' "

    result = subprocess.check_output(
        base_command.format(
            key=key,
            iv=iv,
            invoice=data
        ),
        shell=True, universal_newlines=True
    )
    return result


def encrypt_aes_key(public_key, aes_key):
    public_key = "-----BEGIN PUBLIC KEY-----\n" + \
        public_key + "\n-----END PUBLIC KEY-----"
    key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(key, SHA256)
    ciphertext = cipher.encrypt(aes_key.encode())
    return base64.b64encode(ciphertext).decode()


def sign(data, private_key):
    key = RSA.import_key(private_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return base64.b64encode(signature).decode()
