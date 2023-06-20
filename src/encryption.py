import rsa
import base64


def sign(data, private_key):
    pkey = rsa.PrivateKey.load_pkcs1(private_key)
    sign = rsa.sign(data.encode(), pkey, "SHA-256")
    return base64.b64encode(sign).decode()
