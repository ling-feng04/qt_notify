from Crypto.Cipher import AES
import base64


# AES加密
class AESUtiles:
    def __init__(self):
        self.key = "0CoJUm6Qyw8W8jud"       # 密钥
        self.vi = "0102030405060708"

    def AES_Encrypt(self, key, data):
        pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        data = pad(data)
        # 字符串补位
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        encryptedbytes = cipher.encrypt(data.encode('utf8'))
        # 加密后得到的是bytes类型的数据
        encodestrs = base64.b64encode(encryptedbytes)
        enctext = encodestrs.decode('utf8')
        return enctext

    def AES_Decrypt(self, key, data):
        data = data.encode('utf8')
        encodebytes = base64.decodebytes(data)
        # 将加密数据转换位bytes类型数据
        cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, self.vi.encode('utf8'))
        text_decrypted = cipher.decrypt(encodebytes)
        unpad = lambda s: s[0:-s[-1]]
        text_decrypted = unpad(text_decrypted)
        # 去补位
        text_decrypted = text_decrypted.decode('utf8')
        return text_decrypted