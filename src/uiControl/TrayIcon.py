from PyQt5.QtCore import QTimer, pyqtSignal
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction

from src.fileUtiles.FileUtils import FileUtils
from src.uiControl.NotifyDialog import NotifyDialog
from src.dataScrapy.ToDoTask import ToDoTask


# 托盘设计及控制
class TrayIcon(QSystemTrayIcon):
    signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(TrayIcon, self).__init__(parent)
        self.timerCount = 0
        self.flickerIconTimer = QTimer()
        self.getMessageTimer = QTimer()
        self.setMessageTimer = QTimer()
        self.flickerIconTimer.timeout.connect(self.flickerIcon)
        self.fu = FileUtils()
        self.showMenu()
        self.setMessage()
        self.toDoPrompt()
        self.getParameters()
        self.activated.connect(self.iconClicked)

    # 获取setting.xml中节点用户名和频率参数
    def getParameters(self):
        if len(self.fu.readXML()) > 3:
            self.setToolTip('帐号：' + self.fu.readXML()[0])
            times = self.fu.readXML()[3]
        else:
            times = self.fu.readXML()[1]
        # 定时保存获取系统待办任务至XML文件message节点
        self.setMessageTimer.timeout.connect(self.setMessage)
        self.setMessageTimer.start(int(times) * 60 * 1000)
        # 定时器频率参数分钟/次获取XML文件message节点
        self.getMessageTimer.timeout.connect(self.toDoPrompt)
        self.getMessageTimer.start(int(times) * 60 * 1000 + 1000)

    # 托盘图标闪烁
    def toDoPrompt(self):
        zero = self.isNoneMsg()
        if zero:
                nd = NotifyDialog()
                nd.show()
                nd.exec_()
        else:
            self.setIcon(QIcon("./icon/mainIcon.ico"))
        self.flickerIconTimer.start(1000)

    def showMenu(self):  # 托盘菜单
        menu = QMenu()
        user_action = QAction("切换帐号", self, triggered=self.changeUser)
        user_action.setIcon(QIcon("./icon/changeUser.ico"))
        quit_action = QAction("退出程序", self, triggered=self.quit)
        quit_action.setIcon(QIcon("./icon/exitSys.ico"))
        menu.addAction(user_action)
        menu.addAction(quit_action)
        self.setContextMenu(menu)

    # 鼠标点击操作，key 3：左键单击 2：左键双击 1：右键单击
    def iconClicked(self, key):
        # 鼠标左击闪烁托盘图标
        if key == 3 and self.flickerIconTimer.isActive():
            zero = self.isNoneMsg()
            if zero:
                nd = NotifyDialog()
                nd.show()       # 展示待办任务弹窗
                self.flickerIconTimer.stop()
                self.setIcon(QIcon("./icon/mainIcon.ico"))

    # 切换用户账号
    def changeUser(self):
        pw = self.parent()
        if pw.isVisible():
            pw.hide()
        else:
            pw.show()
        self.hide()
        # 关闭获取待办任务定时器并将xml中待办任务信息置为0
        self.getMessageTimer.stop()
        self.setMessageTimer.stop()
        self.fu.updateMessage("0")

    def quit(self):
        self.setVisible(False)
        sys.exit(0)

    # 闪烁托盘图标
    def flickerIcon(self):
        zero = self.isNoneMsg()
        if zero:
            self.timerCount = self.timerCount + 1
            if self.timerCount % 2:
                self.setIcon(QIcon("./icon/mainIcon.ico"))
            else:
                self.setIcon(QIcon("./icon/noImage.ico"))
        else:
            self.setIcon(QIcon("./icon/mainIcon.ico"))

    # 获取待办事件
    def setMessage(self):
        tdt = ToDoTask()
        info = self.fu.readXML()
        status = tdt.checkUrl()
        if status:
            token = tdt.getToken()
            flag = tdt.checkAccount(info[0], info[1])
            if flag == 0x01:
                num = tdt.getNotify(token)
                self.fu.updateMessage(num)
            else:
                self.fu.updateXML(info[0], "")
                pw = self.parent()
                if pw.isVisible():
                    pw.hide()
                else:
                    pw.show()
                self.signal.emit("请您重新帐号验证！")
                self.hide()
        else:
            self.fu.updateMessage("0")

    # 判断message是否为0
    def isNoneMsg(self):
        info = self.fu.readXML()
        if len(info) == 5:
            if info[4] != "0":
                return True
            else:
                return False
        else:
            return False


