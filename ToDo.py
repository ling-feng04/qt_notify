import sys

from PyQt5 import QtWidgets

from src.uiControl.LoginSys import LoginWindow
from src.fileUtiles.FileUtils import FileUtils
from src.dataScrapy.ToDoTask import ToDoTask


# 程序入口
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    win = LoginWindow()
    f = FileUtils()
    content = f.readXML()
    td = ToDoTask()
    # 非首次登入，需要验证setting文件中的账号密码
    if len(content) == 5:
        status = td.checkUrl()
        if status:
            flag = td.checkAccount(content[0], content[1])
            if flag == 0x01:
                win.hide()
                win.ti.show()
            else:
                win.show()      # 账号密码验证失败返回登入界面
                win.tip.setText("请重新帐号验证！")
                win.password.setText("")
        else:
            win.show()      # 网络连接失败  返回登入界面
            win.tip.setText("服务器连接失败！")
            win.password.setText("")
    elif len(content) == 4:   # 重新验证
        win.show()
        win.tip.setText("请您重新帐号验证！")
        win.password.setText("")
    else:
        win.show()
    sys.exit(app.exec_())