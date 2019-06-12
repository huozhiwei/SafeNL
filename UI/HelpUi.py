# -*- encoding:utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os
import sys

curFolder = os.getcwd()
imagesFolder = "%s\\images" % curFolder[0:curFolder.rfind("\\")]
iconPath = "%s\\images\\icons\\tool.png" % curFolder[0:curFolder.rindex("\\")]
# print(iconPath)
# print(curFolder) # UI
# print(curFolder.rindex("\\"))

class HelpUi(QMainWindow):
    def __init__(self,parent=None):
        super(HelpUi,self).__init__(parent)
        self.setGeometry(600,270,650,430)
        self.setWindowTitle("Help")
        self.setWindowIcon(QIcon(iconPath))
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)
        self.textEdit.setFont(QFont("Times New Roman",13))
        text = "This tool is helped to transform SafeNL Doc to MyCCSL Doc."+ "\n" + "\n"
        text = text + " 1、SafeNL to CCSL" + "\n"
        text = text + "    This step is helped to transform SafeNL to CCSL according to our rules." + "\n"
        text = text + " 2、CCSL to MyCCSL" + "\n"
        text = text + "    This step is helped to transform CCSL to MyCCSL accoding to the rules of MyCCSL." + "\n"

        text = text + "\n"

        self.textEdit.setPlainText(text)
        self.textEdit.setReadOnly(True)
        self.WinAlignCenter()

    # 居中显示
    def WinAlignCenter(self):
        screen = QDesktopWidget().screenGeometry()
        winSize = self.geometry()
        self.move((screen.width()-winSize.width())/2,(screen.height()-winSize.height())/2)

# def main():
#     app = QApplication(sys.argv)
#     helpui = HelpUi()
#     helpui.show()
#     sys.exit(app.exec_())
#
# if __name__=="__main__":
#     main()


