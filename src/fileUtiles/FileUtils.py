import xml.etree.ElementTree as ET

from src.fileUtiles.AESUtiles import AESUtiles


# xml文件读取与更新
class FileUtils:
    def __init__(self):
        self.aes = AESUtiles()
        self.key = self.aes.key
        self.domTree = ET.parse("./setting.xml")
        self.rootNode = self.domTree.getroot()

    def updateXML(self, account, password):
        encAccount = self.aes.AES_Encrypt(self.key, account)
        acc = self.rootNode.find("account")
        acc.text = encAccount
        if password != "":
            encPassword = self.aes.AES_Encrypt(self.key, password)
        else:
            encPassword = ""
        pas = self.rootNode.find("password")
        pas.text = encPassword
        self.domTree.write("./setting.xml", encoding="UTF-8")

    def updateMessage(self, message):
        mess = self.rootNode.find("message")
        mess.text = message
        self.domTree.write("./setting.xml", encoding="UTF-8")

    def readXML(self):
        information = []
        account = self.rootNode.find("account").text
        password = self.rootNode.find("password").text
        if account:
            account = self.aes.AES_Decrypt(self.key, account)
            information.append(account)
        if password:
            password = self.aes.AES_Decrypt(self.key, password)
            information.append(password)
        ip = self.rootNode.find("ip").text
        information.append(ip)
        times = self.rootNode.find("times").text
        information.append(times)
        message = self.rootNode.find("message").text
        information.append(message)
        return information

