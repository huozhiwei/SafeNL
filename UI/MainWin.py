# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtCore import *
from HelpUi import HelpUi
from LayOut import LayOut

# print(sys.path)
class TransMainWin(QMainWindow):
    def __init__(self,parent=None):
        super(TransMainWin,self).__init__(parent)
        # 设置窗口所有控件的风格为['windowsvista', 'Windows', 'Fusion']中的“Windows”,系统默认为"windowsvista"风格
        QApplication.setStyle("Fusion")
        # 设置主窗口
        self.setWindowTitle("SafeNL Trans Tool")
        # 创建状态栏
        self.status = self.statusBar()
        self.status.showMessage("please import a SafeNL document",5000) # 单位ms

        self.helpTextEdit = QTextEdit()

        # 分割成竖着的四块
        # 传入窗口的尺寸
        self.layout = LayOut(self.geometry())
        self.setCentralWidget(self.layout.splitterAll)
        self.layout.completeBtn.clicked.connect(self.showPushSafeNLToCCSLMsg)
        self.layout.safeNLToCCSLBtn.clicked.connect(self.showPushMyCCSLMsg)
        self.layout.CCSLToMyCCSLBtn.clicked.connect(self.showTransMyCCSLMsg)

        bar = self.menuBar()
        self.fileBar = bar.addMenu("File")
        self.fileBar.setFont(QFont("Times New Roman",12))
        openAction = QAction("Open",self)
        # self.fileBar.addAction("Open")
        openAction.setShortcut("Ctrl+O")
        openAction.setFont(QFont("Times New Roman",10))
        self.fileBar.addAction(openAction)
        openAction.triggered.connect(self.openSafeNL)
        # self.fileBar.triggered[QAction].connect(self.openSafeNL)

        # 在菜单栏file中加一条横着的分割线;;菜单添加分割线
        self.fileBar.addSeparator()

        #  疑问：是否真的保存了？？？
        saveAction = QAction("Save",self)
        saveAction.setShortcut("Ctrl+S")
        saveAction.setFont(QFont("Times New Roman",10))
        self.fileBar.addAction(saveAction)
        saveAction.triggered.connect(self.saveFile)
        #self.fileBar.triggered[QAction].connect(self.saveFile)

        self.helpBar = bar.addMenu("Help")
        self.helpBar.setFont(QFont("Times New Roman",12))
        helpAction = QAction("Help",self)
        helpAction.setShortcut("Ctrl+H")
        helpAction.setFont(QFont("Times New Roman",10))
        self.helpBar.addAction(helpAction)
        self.helpBar.triggered[QAction].connect(self.HelpUi)
        # self.helpBar.triggered.connect(self.HelpUi)
        # helpAction.triggered[bool].connect(self.HelpUi)
        # helpAction.triggered.connect(self.HelpUi)

        self.fileBar.addSeparator()
        # Copy
        copyAction = QAction("Copy",self)
        copyAction.setShortcut("Ctrl+C")
        copyAction.setFont(QFont("Times New Roman",10))
        self.fileBar.addAction(copyAction)
        copyAction.triggered.connect(self.copyFile)

        self.fileBar.addSeparator()
        # Paste
        pasteAction = QAction("Paste",self)
        pasteAction.setShortcut("Ctrl+V")
        pasteAction.setFont(QFont("Times New Roman",10))
        self.fileBar.addAction(pasteAction)
        pasteAction.triggered.connect(self.pasteFile)

        self.fileBar.addSeparator()
        # Cut
        cutAction = QAction("Cut",self)
        cutAction.setShortcut("Ctrl+X")
        cutAction.setFont(QFont("Times New Roman",10))
        self.fileBar.addAction(cutAction)
        cutAction.triggered.connect(self.cutFile)

        self.fileBar.addSeparator()
        # Select All
        selectAllAction = QAction("SelectAll",self)
        selectAllAction.setShortcut("Ctrl+A")
        selectAllAction.setFont(QFont("Times New Roman",10))
        self.fileBar.addAction(selectAllAction)
        selectAllAction.triggered.connect(self.selectAllWords)

        self.initUi()

    # 初始化窗口
    def initUi(self):
        curPath = sys.path[0]
        curFolder = curPath[0:curPath.rfind("\\")]
        self.iconPath = "%s\\images\\icons\\tool.png" % curFolder
        self.setGeometry(300,300,250,150) # 初始化位置显示
        # 设置窗口尺寸
        self.resize(1000, 600)
        self.setWindowIcon(QIcon(self.iconPath))
        self.WinAlignCenter()

    # 居中显示
    def WinAlignCenter(self):
        # 获取屏幕坐标系
        screen = QDesktopWidget().screenGeometry()
        # 获取窗口坐标系
        winSize = self.geometry()
        self.move((screen.width()-winSize.width())/2,(screen.height()-winSize.height())/2-50)

    @pyqtSlot()
    def openSafeNL(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setFilter(QDir.Files)
        filename, _ = dlg.getOpenFileName(None,"Open File","./") # 返回绝对路径
        try:
            self.file = open(filename,"r")
            self.data = self.file.read()
            self.layout.leftTextEdit_2.setPlainText(self.data)
        except Exception as e:
            print(e)
        finally:
            if self.file:
                self.file.close()

    def saveFile(self):
        self.status.showMessage("Saving File...",3000) # 单位ms
        # safenlfname, _1 = QFileDialog.getSaveFileName(self, "Save SafeNL File", "./")
        if self.layout.safeNLOld != self.layout.safeNLNew:
            safenlfname, _1 = QFileDialog.getSaveFileName(self,"Save SafeNL File","./")
            self.layout.storesafenlList = []; self.layout.storesafenlset = {}
            self.layout.deletesafenlList = []; self.layout.deletesafenlset = {}
            if safenlfname:
                try:
                    safenldata = self.layout.safeNLNew
                    self.safenlfile = open(safenlfname,"w+",encoding="utf-8")
                    self.safenlfile.write(safenldata)
                    self.layout.safeNLNew = self.layout.safeNLOld
                except Exception as e:
                    print(e)
                finally:
                    if self.safenlfile:
                        self.safenlfile.close()
        if self.layout.CCSLOld != self.layout.CCSLNew:
            CCSLfname, _2 = QFileDialog.getSaveFileName(self,"Save CCSL File","./")
            self.layout.storeCCSLList = []; self.layout.storeCCSLset = {}
            self.layout.deleteCCSLList = []; self.layout.deleteCCSLset = {}
            if CCSLfname:
                try:
                    CCSLdata = self.layout.CCSLNew
                    self.CCSLfile = open(CCSLfname,"w+",encoding="utf-8")
                    self.CCSLfile.write(CCSLdata)
                    self.layout.CCSLNew = self.layout.CCSLOld
                except Exception as e:
                    print(e)
                finally:
                    if self.CCSLfile:
                        self.CCSLfile.close()
        if self.layout.MyCCSLOld != self.layout.MyCCSLNew:
            MyCCSLfname, _3 = QFileDialog.getSaveFileName(self,"Save MyCCSL File","./")
            if MyCCSLfname:
                try:
                    MyCCSLdata = self.layout.MyCCSLNew
                    self.MyCCSLfile = open(MyCCSLfname,"w+",encoding="utf-8")
                    self.MyCCSLfile.write(MyCCSLdata)
                    self.layout.MyCCSLNew = self.layout.MyCCSLOld
                except Exception as e:
                    print(e)
                finally:
                    if self.MyCCSLfile:
                        self.MyCCSLfile.close()

    def copyFile(self):
        pass

    def pasteFile(self):
        pass

    def cutFile(self):
        pass

    def selectAllWords(self):
        pass

    def showPushSafeNLToCCSLMsg(self):
        self.status.showMessage("please push 'SafeNL->CCSL' button.",3000) # 3000ms

    def showPushMyCCSLMsg(self):
        self.status.showMessage("transforming SafeNL->CCSL...",3000)

    def showTransMyCCSLMsg(self):
        self.status.showMessage("transfroming CCSL->MyCCSL...",3000)

    def HelpUi(self):
        self.helpTextEdit.setPlainText("")
        self.helpui = HelpUi()
        self.helpui.show()

def main():
    app = QApplication(sys.argv)
    transMainWin = TransMainWin()
    transMainWin.show()
    # 进入程序主循环
    sys.exit(app.exec_())

if __name__=="__main__":
    main()
