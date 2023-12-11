import sys

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QCursor
import ctypes

from PyQt5.QtWidgets import QMessageBox

from ui.LoginUI import Ui_Form
from src.uiControl.TrayIcon import TrayIcon
from src.fileUtiles.FileUtils import FileUtils
from src.dataScrapy.ToDoTask import ToDoTask


# 程序登入界面控制
class LoginWindow(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(LoginWindow, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon('./icon/mainIcon.ico'))
        self.tip.setStyleSheet("color:red;")
        self.exitBtn.setStyleSheet("QPushButton:hover{background-color:red}")
        self.tip.setText("")
        self.loginBtn.setShortcut(Qt.Key_Return)
        self.logo.setPixmap(QtGui.QPixmap("./icon/logo.jpg"))
        self.logo.setScaledContents(True)
        # self.loginBtn.setShortcut(Qt.Key_Enter)
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")
        self.f = FileUtils()
        if len(self.f.readXML()) > 3:
            self.ti = TrayIcon(self)
            self.ti.signal.connect(self.reInput)
        self.showUser()

    # 登入按钮事件（第一次登入和账号切换）
    def loginEvent(self):
        td = ToDoTask()
        account = self.account.text()
        password = self.password.text()
        status = td.checkUrl()
        if status:
            if account == "" and password == "":
                self.tip.setText("请输入您的用户帐号和密码！")
            elif account == "":
                self.tip.setText("请输入您的用户帐号！")
            elif password == "":
                self.tip.setText("请输入您的密码！")
            else:
                flag = td.checkAccount(account, password)
                if flag == 0x01:  # 密码正确，界面隐藏托盘并将账号密码保存xml配置文件
                    self.tip.setText("")
                    self.f.updateXML(account, password)
                    self.hide()
                    ti = TrayIcon(self)
                    ti.show()
                elif flag == 0x02:
                    self.tip.setText("您输入的帐号或密码错误！")  # 提示账号或密码错误
                    self.password.setText("")
                else:
                    self.tip.setText("密码输入错误5次，帐户锁定10分钟！")
                    self.password.setText("")
        else:
            self.tip.setText("服务器连接失败！")

    def hideEvent(self, event):  # 最小化操作，缩小化回到任务栏
        self.hide()

    def closeEvent(self, event):
        quitMsgBox = QMessageBox()
        quitMsgBox.setWindowTitle('退出程序提示')
        quitMsgBox.setText('退出待办任务小程序？')
        quitMsgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = quitMsgBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = quitMsgBox.button(QMessageBox.No)
        buttonN.setText('取消')
        quitMsgBox.exec_()
        if quitMsgBox.clickedButton() == buttonY:
            sys.exit(0)
        else:
            pass

    def showUser(self):
        f = FileUtils()
        userInfo = f.readXML()
        if len(userInfo) == 5:
            self.account.setText(userInfo[0])
            self.password.setText(userInfo[1])
        elif len(userInfo) == 4:
            self.account.setText(userInfo[0])

    def reInput(self, msg):
        self.tip.setText(msg)
        self.password.setText("")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            # self.setCursor(QCursor(Qt.PointingHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False
        self.setCursor(QCursor(Qt.ArrowCursor))

