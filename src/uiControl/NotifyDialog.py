from PyQt5 import QtWidgets
from PyQt5.QtCore import QPropertyAnimation, QPoint, QTimer, pyqtSlot, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDesktopWidget

from ui.NotifyUI import Ui_Dialog
from src.fileUtiles.FileUtils import FileUtils


# 消息弹窗动画提醒
class NotifyDialog(QtWidgets.QDialog, Ui_Dialog):

    def __init__(self, parent=None):
        super(NotifyDialog, self).__init__(parent)
        self.remainTimer = QTimer()
        self.setupUi(self)
        self.setWindowIcon(QIcon('./icon/tipDialog.ico'))
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.SHADOW_WIDTH = 40
        self.desktop = QDesktopWidget()
        self.move((self.desktop.availableGeometry().width() - self.width() - 20),
                  self.desktop.availableGeometry().height())  # 初始化位置到右下角
        self.f = FileUtils()
        self.showAnimation()

    # 弹出动画
    def showAnimation(self):
        self.animation = QPropertyAnimation(self, b'pos')
        self.animation.setDuration(1000)
        self.animation.setStartValue(QPoint(self.x(), self.y()))
        self.animation.setEndValue(QPoint((self.desktop.availableGeometry().width() - self.width() - 20), (
                self.desktop.availableGeometry().height() - self.height() - self.SHADOW_WIDTH)))
        self.animation.start()
        content = self.f.readXML()
        if len(content) == 5:
            user = content[0]
            ip = content[2]
            message = content[4]
            self.notify.setText('亲爱的用户：<br>&nbsp;&nbsp;<a href="' + ip + '/login">您有' + message + '条待办任务未处理！</a>')
            self.notify.setOpenExternalLinks(True)

        self.remainTimer.timeout.connect(self.closeAnimation)
        self.remainTimer.start(5000)

    # 关闭动画
    @pyqtSlot()
    def closeAnimation(self):
        # 清除Timer和信号槽
        self.remainTimer.stop()
        self.remainTimer.timeout.disconnect(self.closeAnimation)
        self.remainTimer.deleteLater()
        self.remainTimer = None
        # 弹出框渐隐
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setDuration(1000)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start()
        # 动画完成后清理
        self.animation.finished.connect(self.clearAll)

    # 弹窗隐藏
    @pyqtSlot()
    def clearAll(self):
        self.hide()
        self.animation.finished.disconnect(self.clearAll)
