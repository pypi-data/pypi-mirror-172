from Crypto.Cipher import AES


def encrypt(msg: bytes, d2l_key: bytes, d2l_iv: bytes):
    cipher = AES.new(d2l_key, AES.MODE_CBC, d2l_iv)
    return cipher.encrypt(msg)


def decrypt(msg: bytes, d2l_key: bytes, d2l_iv: bytes) -> bytes:
    cipher = AES.new(d2l_key, AES.MODE_CBC, d2l_iv)
    return cipher.decrypt(msg)
