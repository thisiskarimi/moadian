import base64
import json
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from .xor import XOR


def xor_and_encrypt_data(data, key, iv):
    if not isinstance(key, bytes):
        key = bytes.fromhex(key)
    if not isinstance(iv, bytes):
        iv = bytes.fromhex(iv)
    if not isinstance(data, str):
        data = json.dumps(data)
    text_data = data.encode("utf-8")
    xor_text = XOR().do_xor(text_data, key)
    cipher = AES.new(key, AES.MODE_GCM, nonce=iv)
    ciphertext, tag = cipher.encrypt_and_digest(xor_text)
    return base64.b64encode(ciphertext + tag).decode()


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
