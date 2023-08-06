from Crypto.Util.Padding import pad
from Crypto.Cipher import DES
import binascii


class DES_ECB:

    def __init__(self, key):

        key = key.encode('utf8')
        key = key[:8] if len(key) >= 8 else key + (8-len(key))*b'\0'
        print(key)
        self.cipher = DES.new(key, DES.MODE_ECB)

    def encrypt(self, text):
        ct = self.cipher.encrypt(pad(text.encode('utf8'), 8))
        return binascii.b2a_base64(ct).decode('utf8').strip()

    def decrypt(self, text):
        text = binascii.a2b_base64(text)
        ct = self.cipher.decrypt(text)
        return ct.decode('utf8').strip()
