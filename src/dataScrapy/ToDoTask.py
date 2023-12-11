import json

import urllib.request
import requests
from bs4 import BeautifulSoup

from src.fileUtiles.FileUtils import FileUtils


# 账号验证与获取待办任务类（爬虫）
class ToDoTask:

    def __init__(self):
        self.ip = self.getIp()
        self.listUrl = self.ip + "/system/flowlistAu"
        self.loginUrl = self.ip + "/loginFor"
        self.session = requests.session()

    @staticmethod
    def getIp():
        fu = FileUtils()
        info = fu.readXML()
        if len(info) == 5:
            ip = info[2]
        elif len(info) == 4:
            ip = info[1]
        else:
            ip = info[0]
        return ip

    def checkUrl(self):
        try:
            opener = urllib.request.build_opener()
            opener.open(self.loginUrl, timeout=2)
            return True
        except Exception as e:
            print(e)
            return False

    # 登入页获取xtoken值
    def getToken(self):
        res = self.session.get(self.loginUrl)
        soup = BeautifulSoup(res.text, 'lxml')
        token = soup.input['value']
        return token

    # 系统账号验证
    def checkAccount(self, username, password):
        userData = {'username': username,
                    'password': password}
        response = self.session.post(self.loginUrl, data=userData)
        if response.json().get('code') == 0:
            return 0x01
        else:
            msg = response.json().get('msg')
            if msg.find("帐户锁定") == 9:
                return 0x03
            else:
                return 0x02

    # 获取待办任务列表页
    def getNotify(self, token):
        cookies_dict = requests.utils.dict_from_cookiejar(self.session.cookies)
        headers = {"xtoken": token,
                   "Content-Type": "application/json"}
        data = {"isAsc": "asc",
                "orderByColumn": "",
                "pageNum": 1,
                "productTypeTemporary": ""}
        listRes = self.session.post(self.listUrl, json.dumps(data), headers=headers)
        num = listRes.json().get("total")
        return str(num)

# if __name__ == "__main__":
#     task = ToDoTask()
#     task.checkUrl()
# token = task.getToken()
# if token:
#     flag = task.checkAccount("10011", "111111")
#     if flag:
#         print(task.getNotify())
# else:
#     print("请检查网络连接")
