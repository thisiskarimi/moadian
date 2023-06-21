import base64
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def encrypt_aes_key(public_key, aes_key):
    public_key = "-----BEGIN PUBLIC KEY-----\n" + public_key + "\n-----END PUBLIC KEY-----" 
    key = RSA.importKey(public_key)
    cipher = PKCS1_OAEP.new(key, SHA256)
    ciphertext = cipher.encrypt(aes_key.encode())
    return base64.b64encode(ciphertext).decode()


def sign(data, private_key):
    key = RSA.import_key(private_key)
    h = SHA256.new(data.encode())
    signature = pkcs1_15.new(key).sign(h)
    return base64.b64encode(signature).decode()
