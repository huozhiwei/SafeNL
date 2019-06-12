# -*- coding:utf-8 -*-
import sys
import os
import re
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from SetText import setStepText
from ProcessCCSL import ProcessCCSL
from ProcessSafeNL import ProcessSafeNL
from Process.SafeNLToCCSL import ToCCSL
from ComboBoxItem import setSafeNLCb,setCCSLCb,safenlKw,CCSLKw
from Process.CCSLToMyCCSL import CCSLToMyCCSL,MyCCSLConsList,initAll
from Process.ProcessSpecialStaEve import ProcessSpecialStaEve

curFolder = os.getcwd()
imagesFolder = "%s\\images" % curFolder[0:curFolder.rfind("\\")]
iconPath = "%s\\images\\icons\\tool.png" % curFolder[0:curFolder.rfind("\\")]

class LayOut(QWidget):
    def __init__(self,MainWinSize):
        super(LayOut,self).__init__()
        self.setWindowIcon(QIcon(iconPath))
        self.MainWinSize = MainWinSize
        self.setLayOut()

    def setLayOut(self):
        # 切分的中心面板宽度，4等分
        MainWinWidth = self.MainWinSize.width()/4
        MainWinHeight = self.MainWinSize.height()
        self.left_1 = QFrame()
        self.left_1.setFrameShape(QFrame.StyledPanel)
        self.left_2 = QFrame()
        self.left_2.setFrameShape(QFrame.StyledPanel)
        self.right_1 = QFrame()
        self.right_1.setFrameShape(QFrame.StyledPanel)
        self.right_2 = QFrame()
        self.right_2.setFrameShape(QFrame.StyledPanel)

        self.leftSplitter_1 = QSplitter(Qt.Vertical)
        self.leftSplitter_1.addWidget(self.left_1)
        vleftLayout_1 = QVBoxLayout()
        self.leftTextEdit_1 = QTextEdit()
        self.leftTextEdit_1.setHtml(setStepText())
        self.leftTextEdit_1.setFont(QFont("Times New Roman"))
        self.leftTextEdit_1.setReadOnly(True)
        vleftLayout_1.addWidget(self.leftTextEdit_1)

        # ComboBox relatives
        gridConstrans = QGridLayout()
        gridConstrans.setSpacing(5) # 设置控件在水平和垂直方向的间隔
        self.tiplb = QLabel("<b>External Constrans:</b>")
        self.tiplb.setFont(QFont("Times New Roman",9))
        self.safenlcb = QComboBox()
        self.safenlcb.setFont(QFont("Times New Roman",9))
        safenlkwList = setSafeNLCb()
        self.safenlcb.addItems(safenlkwList)
        self.safenlcb.activated.connect(self.confirmsafenlexample)
        self.safenlLineEdit = QLineEdit()
        self.safenlLineEdit.setPlaceholderText("Input SafeNL")
        self.safenlLineEdit.setFont(QFont("Times New Roman", 9, -1, True))
        self.safenlLineEdit.editingFinished.connect(self.storeextrasafenl)
        self.safenlLineEdit.editingFinished.connect(self.deleteneededsafenl)
        self.CCSLcb = QComboBox()
        self.CCSLcb.setFont(QFont("Times New Roman",9))
        CCSLkwList = setCCSLCb()
        self.CCSLcb.addItems(CCSLkwList)
        self.CCSLcb.activated.connect(self.confirmCCSLexample)
        self.ccslLineEdit = QLineEdit()
        self.ccslLineEdit.setPlaceholderText("Input CCSL")
        self.ccslLineEdit.setFont(QFont("Times New Roman", 9, -1, True))
        self.ccslLineEdit.editingFinished.connect(self.storeextraCCSL)
        self.ccslLineEdit.editingFinished.connect(self.deleteneededCCSL)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.setToolTip("Push <b>'Delete'</b> to delete Constrans")
        self.deleteBtn.setFont(QFont("Times New Roman",9))
        self.deleteBtn.clicked.connect(self.deleteSafeNL)
        self.deleteBtn.clicked.connect(self.deleteCCSL)
        self.completeBtn = QPushButton("Complete")
        self.completeBtn.setToolTip("Push <b>'Complete'</b> to end Input")
        self.completeBtn.setFont(QFont("Times New Roman",9))
        self.completeBtn.clicked.connect(self.safenlToCCSLOn)
        self.completeBtn.clicked.connect(self.updateSafeNL)
        self.completeBtn.clicked.connect(self.updateCCSL)
        self.storesafenlList = [];self.storesafenlset = {}
        self.storeCCSLList = [];self.storeCCSLset = {}
        self.deletesafenlList = []; self.deletesafenlset = {}
        self.deleteCCSLList = [];self.deleteCCSLset = {}
        gridConstrans.addWidget(self.tiplb,0,0)
        gridConstrans.addWidget(self.safenlcb,1,0)
        gridConstrans.addWidget(self.safenlLineEdit,1,1)
        gridConstrans.addWidget(self.CCSLcb,2,0)
        gridConstrans.addWidget(self.ccslLineEdit,2,1)
        gridConstrans.addWidget(self.deleteBtn,3,0)
        gridConstrans.addWidget(self.completeBtn,3,1)
        tmpWid = QWidget()
        tmpWid.setLayout(gridConstrans)
        vleftLayout_1.addWidget(tmpWid)

        self.safeNLToCCSLBtn = QPushButton("SafeNL->CCSL")
        self.safeNLToCCSLBtn.setCheckable(True)
        self.safeNLToCCSLBtn.setFont(QFont("Times New Roman",12))
        self.safeNLToCCSLBtn.setEnabled(False)
        self.safeNLToCCSLBtn.clicked.connect(self.showCCSLResultMsg)
        self.safeNLToCCSLBtn.clicked.connect(self.CCSLToMyCCSLOn)
        vleftLayout_1.addWidget(self.safeNLToCCSLBtn)

        self.CCSLToMyCCSLBtn = QPushButton("CCSL->MyCCSL")
        self.CCSLToMyCCSLBtn.setFont(QFont("Times New Roman",12))
        self.CCSLToMyCCSLBtn.setEnabled(False)
        self.CCSLToMyCCSLBtn.clicked.connect(self.showMyCCSLResultMsg)
        vleftLayout_1.addWidget(self.CCSLToMyCCSLBtn)

        self.left_1.setLayout(vleftLayout_1)
        self.leftSplitter_1.addWidget(self.left_1)
        self.leftSplitter_1.setSizes([MainWinHeight,])

        '''
        Sets the child widgets' respective sizes to the values given in the list. 
        If the splitter is horizontal, the values set the width of each widget in pixels, from left to right. 
        If the splitter is vertical, the height of each widget is set, from top to bottom.
        '''
        self.leftSplitter_2 = QSplitter(Qt.Vertical)
        self.leftTextEdit_2 = QTextEdit()
        self.leftTextEdit_2.setReadOnly(True)
        self.leftTextEdit_2.setFont(QFont("Times New Roman",9))
        self.safeNLNew = "";self.safeNLOld = ""
        if self.leftTextEdit_2.toPlainText() != "":
            self.safeNLNew = self.leftTextEdit_2.toPlainText()
        self.leftTextEdit_2.textChanged.connect(self.safeNLText)
        # self.leftTextEdit_2.cursorPositionChanged.connect(self.safeNLText)
        self.leftTextEdit_2.setPlaceholderText("SafeNL Doc.")
        hLeftLayout_2 = QHBoxLayout()
        hLeftLayout_2.addWidget(self.leftTextEdit_2)
        self.left_2.setLayout(hLeftLayout_2)
        self.leftSplitter_2.addWidget(self.left_2)
        self.leftSplitter_2.setSizes([MainWinHeight, ])

        self.rightSplitter_1 = QSplitter(Qt.Vertical)
        self.rightTextEdit_1 = QTextEdit()
        self.rightTextEdit_1.setReadOnly(True)
        self.rightTextEdit_1.setFont(QFont("Times New Roman",9))
        self.CCSLNew = "";self.CCSLOld = ""
        if self.rightTextEdit_1.toPlainText() != "":
            self.CCSLNew = self.rightTextEdit_1.toPlainText()
        self.rightTextEdit_1.textChanged.connect(self.CCSLText)
        # self.rightTextEdit_1.cursorPositionChanged.connect(self.CCSLText)
        self.rightTextEdit_1.setPlaceholderText("CCSL Doc.")
        hRightLayout_1 = QHBoxLayout()
        hRightLayout_1.addWidget(self.rightTextEdit_1)
        self.right_1.setLayout(hRightLayout_1)
        self.rightSplitter_1.addWidget(self.right_1)
        self.rightSplitter_1.setSizes([MainWinHeight, ])

        self.rightSplitter_2 = QSplitter(Qt.Vertical)
        self.rightTextEdit_2 = QTextEdit()
        self.rightTextEdit_2.setReadOnly(True)
        self.rightTextEdit_2.setFont(QFont("Times New Roman",9))
        self.MyCCSLNew = "";self.MyCCSLOld = ""
        if self.rightTextEdit_2.toPlainText() != "":
            self.MyCCSLNew = self.rightTextEdit_2.toPlainText()
        self.rightTextEdit_2.textChanged.connect(self.MyCCSLText)
        # self.rightTextEdit_2.cursorPositionChanged.connect(self.MyCCSLText)
        self.rightTextEdit_2.setPlaceholderText("MyCCSL Doc.")
        hRightLayout_2 = QHBoxLayout()
        hRightLayout_2.addWidget(self.rightTextEdit_2)
        self.right_2.setLayout(hRightLayout_2)
        self.rightSplitter_2.addWidget(self.right_2)
        self.rightSplitter_2.setSizes([MainWinHeight, ])

        self.splitterAll = QSplitter(Qt.Horizontal)
        self.splitterAll.addWidget(self.leftSplitter_1)
        self.splitterAll.addWidget(self.leftSplitter_2)
        self.splitterAll.addWidget(self.rightSplitter_1)
        self.splitterAll.addWidget(self.rightSplitter_2)
        self.splitterAll.setSizes([MainWinWidth,MainWinWidth,MainWinWidth,MainWinWidth])

    # @pyqtSlot()
    # 此slot函数不能加@pyqtSlot()
    def confirmsafenlexample(self,cursafenlitemIndex):
        # print(str(cursafenlitemIndex),self.safenlcb.currentText())
        if self.safenlcb.currentText() == "imply":
            self.safenlLineEdit.setText("obj1.attr1.state1 imply obj2.attr2.state2")
        elif self.safenlcb.currentText() == "exclude":
            self.safenlLineEdit.setText("obj1.attr1.state1 exclude obj2.attr2.state2")
        elif self.safenlcb.currentText() == "permit":
            self.safenlLineEdit.setText("obj1.attr1.state1 permit obj2.attr2.event1")
        elif self.safenlcb.currentText() == "forbid":
            self.safenlLineEdit.setText("obj1.attr1.state1 forbid obj2.attr2.event1")
        elif self.safenlcb.currentText() == "trigger":
            self.safenlLineEdit.setText("obj2.attr2.event2 trigger obj1.attr1.state1 in t1(30 ms)")
        elif self.safenlcb.currentText() == "terminate":
            self.safenlLineEdit.setText("obj2.attr2.event2 terminate obj1.attr1.state1 in t1(30 ms)")
        else:
            self.safenlLineEdit.setText("obj1.attr1.event1 within t1([0,30]s) forbid obj.attr2.event2")

    # @pyqtSlot()
    # 此slot函数不能加@pyqtSlot()
    def confirmCCSLexample(self,curCCSLitemIndex):
        if self.CCSLcb.currentText() == "<":
            self.ccslLineEdit.setText("C1 < C2")
        elif self.CCSLcb.currentText() == "≤":
            self.ccslLineEdit.setText("C1 ≤ C2")
        elif self.CCSLcb.currentText() == "sup":
            self.ccslLineEdit.setText("C = sup(C1,C2,C3)")
        elif self.CCSLcb.currentText() == "inf":
            self.ccslLineEdit.setText("C = inf(C1,C2,C3)")
        elif self.CCSLcb.currentText() == "~":
            self.ccslLineEdit.setText("C1 ~ C2")
        elif self.CCSLcb.currentText() == "🗲":
            self.ccslLineEdit.setText("C1 = C2 🗲 C3")
        elif self.CCSLcb.currentText() == "==":
            self.ccslLineEdit.setText("C1 == C2")
        elif self.CCSLcb.currentText() == "-":
            self.ccslLineEdit.setText("i ≤ C1 - C2 ≤ j")
        elif self.CCSLcb.currentText() == "#":
            self.ccslLineEdit.setText("C1 # C2")
        else:
            self.ccslLineEdit.setText("C1 = C2 $d on C3")

    def popRetryMsgBox(self,flag):
        title = "Wrong Format"
        if not flag:
            text = "SafeNL Wrong Format! Please input again."
        else:
            text = "CCSL Wrong Format! Please input again."
        retryMsgBox = \
            QMessageBox.critical(self, title, text, QMessageBox.Retry, QMessageBox.Retry)

    @pyqtSlot()
    def deleteneededsafenl(self):
        safenltmpstr = self.safenlLineEdit.text()
        newList = []
        for safenltmp in safenlKw:
            # re.search()匹配成功返回一个匹配的对象，否则返回None
            if re.search("\s+" + safenltmp + "\s+", safenltmpstr) != None:
                    newList.append(safenltmpstr)
        if newList:
            self.deletesafenlList.append(safenltmpstr)
        else:
            if self.safenlLineEdit.text() and self.safenlLineEdit.text() != "":
                self.popRetryMsgBox(0)

    @pyqtSlot()
    def deleteneededCCSL(self):
        CCSLtmpstr = self.ccslLineEdit.text()
        newList = []
        for CCSLtmp in CCSLKw:
            # 匹配成功返回一个匹配的对象，否则返回None
            if CCSLtmp != "sup" and CCSLtmp != "inf" and CCSLtmp != "$":
                if re.search("\s+" + CCSLtmp + "\s+", CCSLtmpstr) != None:
                    newList.append(CCSLtmpstr)
            else:
                if CCSLtmp == "$":
                    CCSLtmp = '\\' + CCSLtmp
                    if re.search("\s+" + CCSLtmp + "\S+", CCSLtmpstr) != None:
                        newList.append(CCSLtmpstr)
                else:
                    if re.search("\s+" + CCSLtmp + "\S+", CCSLtmpstr) != None:
                        newList.append(CCSLtmpstr)
        if newList:
            self.deleteCCSLList.append(CCSLtmpstr)
        else:
            if self.ccslLineEdit.text() and self.ccslLineEdit.text() != "":
                self.popRetryMsgBox(1)

    @pyqtSlot()
    def deleteSafeNL(self):
        self.deletesafenlset = set(self.deletesafenlList)
        # print(self.deletesafenlList)
        tmpList = self.leftTextEdit_2.toPlainText().split(";")
        for i, tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        tmpexList = []
        for tmpdeleteset in self.deletesafenlset:
            if tmpdeleteset in tmpList:
                tmpexList.append(tmpdeleteset)
        tmpList_1 = []
        for tmp in tmpList:
            if tmp and not tmp.isspace():
                tmpList_1.append(tmp)
        tmpList = tmpList_1;tmpstr = ""
        for tmp in tmpList:
            if tmp not in tmpexList:
                tmpstr = tmpstr + tmp + ";\n"
        self.leftTextEdit_2.setPlainText(tmpstr)
        self.storesafenlList = []
        # self.deletesafenlList = []

    @pyqtSlot()
    def deleteCCSL(self):
        self.deleteCCSLset = set(self.deleteCCSLList)
        # print(self.deleteCCSLList)
        tmpList = self.rightTextEdit_1.toPlainText().split(";")
        for i, tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        tmpexList = []
        for tmpdeleteset in self.deleteCCSLset:
            if tmpdeleteset in tmpList:
                tmpexList.append(tmpdeleteset)
        tmpList_1 = []
        for tmp in tmpList:
            if tmp and not tmp.isspace():
                tmpList_1.append(tmp)
        tmpList = tmpList_1;tmpstr = ""
        for tmp in tmpList:
            if tmp not in tmpexList:
                tmpstr = tmpstr + tmp + ";\n"
        self.rightTextEdit_1.setPlainText(tmpstr)
        self.storeCCSLList = []
        # self.deleteCCSLList = []

    @pyqtSlot()
    def storeextrasafenl(self):
        safenltmpstr = self.safenlLineEdit.text()
        newList = []
        for safenltmp in safenlKw:
            # re.search()匹配成功返回一个匹配的对象，否则返回None
            if re.search("\s+" + safenltmp + "\s+", safenltmpstr) != None:
                newList.append(safenltmpstr)
        if newList:
            self.storesafenlList.append(safenltmpstr)
        else:
            # self.popRetryMsgBox()
            pass

    @pyqtSlot()
    def storeextraCCSL(self):
        CCSLtmpstr = self.ccslLineEdit.text()
        newList = []
        for CCSLtmp in CCSLKw:
            # 匹配成功返回一个匹配的对象，否则返回None
            if CCSLtmp != "sup" and CCSLtmp != "inf" and CCSLtmp != "$":
                if re.search("\s+" + CCSLtmp + "\s+", CCSLtmpstr) != None:
                    newList.append(CCSLtmpstr)
            else:
                if CCSLtmp == "$":
                    CCSLtmp = '\\' + CCSLtmp
                    if re.search("\s+" + CCSLtmp + "\S+", CCSLtmpstr) != None:
                        newList.append(CCSLtmpstr)
                else:
                    if re.search("\s+" + CCSLtmp + "\S+", CCSLtmpstr) != None:
                        newList.append(CCSLtmpstr)
        if newList:
            self.storeCCSLList.append(CCSLtmpstr)
        else:
            # self.popRetryMsgBox()
            pass

    def processDuplicatedSafeNL(self,tmpList):
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        tmpList_1 = tmpList
        tmpList = sorted(set(tmpList_1), key=tmpList_1.index)
        tmpList_1 = []
        for tmp in tmpList:
            if tmp and not tmp.isspace():
                tmpList_1.append(tmp + ";")
        tmpList = tmpList_1
        tmpstr = ""
        for tmp in tmpList:
            tmpstr = tmpstr + tmp + "\n"
        return tmpstr

    @pyqtSlot()
    def updateSafeNL(self):
        self.storesafenlset = set(self.storesafenlList)
        tmpList = self.leftTextEdit_2.toPlainText().split(";")
        tmpexList = []
        for tmpstoreset in self.storesafenlset:
            if tmpstoreset not in tmpList:
                tmpexList.append(tmpstoreset)
        tmpList.extend(tmpexList)
        tmpstr = self.processDuplicatedSafeNL(tmpList)
        self.leftTextEdit_2.setPlainText(tmpstr)
        # 在SafeNL面板上加上互斥的state和event
        leftTextEdit_2 = self.leftTextEdit_2.toPlainText()
        tmpProcesssafeNL = ProcessSafeNL(leftTextEdit_2)
        process_special_sta_eve = ProcessSpecialStaEve()
        tmpList = (leftTextEdit_2 + ProcessSpecialStaEve.constraintToBeInStr).split(";")
        tmpstr = self.processDuplicatedSafeNL(tmpList)
        self.leftTextEdit_2.setPlainText(tmpstr)
        # self.storesafenlList = []
        self.deletesafenlList = []
        ToCCSL.initConstraint()
        ProcessSpecialStaEve.AllClear()

    @pyqtSlot()
    def updateCCSL(self):
        self.storeCCSLset = set(self.storeCCSLList)
        tmpList = self.rightTextEdit_1.toPlainText().split(";")
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        tmpexList = []
        for tmpstoreset in self.storeCCSLset:
            if tmpstoreset not in tmpList:
                tmpexList.append(tmpstoreset)
        tmpList_1 = []
        for tmpex in tmpexList:
            if tmpex and not tmpex.isspace():
                tmpList_1.append(tmpex + ";")
        tmpstr = ""
        for tmpex in tmpList_1:
            tmpstr = tmpstr + tmpex + "\n"
        self.neededappendstr = tmpstr
        tmpList.extend(tmpexList)
        tmpList_1 = []
        for tmp in tmpList:
            if tmp and not tmp.isspace():
                tmpList_1.append(tmp + ";")
        tmpList = tmpList_1;tmpstr = ""
        for tmp in tmpList:
            tmpstr = tmpstr + tmp + "\n"
        self.rightTextEdit_1.setPlainText(tmpstr)
        self.deleteCCSLList = []
        # self.storeCCSLList = []

    @pyqtSlot()
    def safenlToCCSLOn(self):
        self.safeNLToCCSLBtn.setEnabled(True)

    @pyqtSlot()
    def CCSLToMyCCSLOn(self):
        self.CCSLToMyCCSLBtn.setEnabled(True)

    @pyqtSlot()
    def showCCSLResultMsg(self):
        # 传参数到processSafeNL
        self.processsafeNL = ProcessSafeNL(self.leftTextEdit_2.toPlainText())
        constransList = ToCCSL.constraint.split(";")
        text = ""
        constransList_1 = []
        for i,constranstmp in enumerate(constransList):
            if constranstmp and not constranstmp.isspace():
                constransList_1.append(constranstmp)
        constransList = constransList_1
        for constranstmp in constransList:
            text = text + constranstmp + ";\n"
        text = text + self.neededappendstr
        self.rightTextEdit_1.setPlainText(text)
        ToCCSL.initConstraint()

    @pyqtSlot()
    def showMyCCSLResultMsg(self):
        self.storesafenlList = []; self.storeCCSLList = []
        self.deletesafenlList = []; self.deleteCCSLList = []
        self.processCCSLList = self.rightTextEdit_1.toPlainText().split(";")
        processCCSLList = []
        for i,processCCSLtmp in enumerate(self.processCCSLList):
            if processCCSLtmp and not processCCSLtmp.isspace():
                processCCSLList.append(processCCSLtmp.strip())
        self.processCCSLList = processCCSLList
        for i,processCCSLtmp in enumerate(self.processCCSLList):
            CCSLToMyCCSL(processCCSLtmp)
        text = ""
        for i,MyCCSLConstmp in enumerate(MyCCSLConsList):
            text = text + ProcessCCSL(MyCCSLConstmp)
        self.rightTextEdit_2.setPlainText(text)
        initAll()

    @pyqtSlot()
    def safeNLText(self):
        self.safeNLOld = self.safeNLNew
        self.safeNLNew = self.leftTextEdit_2.toPlainText()

    @pyqtSlot()
    def CCSLText(self):
        self.CCSLOld = self.CCSLNew
        self.CCSLNew = self.rightTextEdit_1.toPlainText()

    @pyqtSlot()
    def MyCCSLText(self):
        self.MyCCSLOld = self.MyCCSLNew
        self.MyCCSLNew = self.rightTextEdit_2.toPlainText()

# def main():
#     app = QApplication(sys.argv)
#     layout = LayOut(MainWinSize)
#     layout.show()
#     sys.exit(app.exec_())
#
# if __name__=="__main__":
#     main()
