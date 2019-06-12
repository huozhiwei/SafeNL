"""
    该部分是用来处理Xtext文件到CCSL文件转换的，其中包含多个状态intersect的中间处理过程：
    obj1.attr1.state1 imply obj2.attr2.state2;
    obj1.attr1.state1 exclude obj2.attr2.state2;
    
    obj1.attr1.state1 permit event1(obj2.attr2.event2);
    obj1.attr1.state1 forbid event1(obj2.attr2.event2);
    event1(obj2.attr2..event2) trigger obj1.attr1.state1 in t1;
    event1(obj2.attr2.event2) terminate obj1.attr1.state1 in t1;
    event1(obj1.attr1.event1) within t1 forbid event2(obj2.attr2.event2);
"""

# -*- coding: utf-8 -*-
import sys
import re
from Process.CCSLToMyCCSL import CCSLKeywords

# "within" 必须在 "forbid"前
basicKwd = ["within","imply","exclude","permit","trigger","terminate","forbid"]
compositeKwd = ["and","or"]

class ToCCSL(object):
    constraint = ""
    countTmp = 1
    stateCount = 1
    allState = []
    allEvent = []

    def __init__(self,keywd,*args):
        self.left = "left"
        self.right = "right"
        self.keywd = keywd
        # self.constraint = ""
        if args:
            self.time = args[0]
            if self.keywd == "within":
                self.keywd_2 = args[1]
        else:
            self.time = "0"

    @classmethod
    def initConstraint(cls):
        cls.constraint = ""
        cls.countTmp = 1
        cls.stateCount = 1
        cls.allState.clear()
        cls.allEvent.clear()

    def replaceWord(self, left, right, keywd, *args):
        self.left = left
        self.right = right
        self.keywd = keywd
        if args:
            self.time = args[0]
            if self.keywd == "within":
                self.keywd_2 = args[1]

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getKeywd(self):
        if self.keywd == "trigger" or self.keywd == "terminate":
            return self.keywd, self.time
        elif self.keywd == "within":
            return self.keywd, self.time, self.keywd_2
        else:
            return self.keywd

    def safeNLToCCSL(self):
        if self.keywd == "imply":
            ToCCSL.constraint += self.right + ".begin" + " ≤ "+ self.left + ".begin;"
            ToCCSL.constraint += self.left + ".end" + " ≤ " + self.right + ".end;"
            ToCCSL.allState.append(self.left)
            ToCCSL.allState.append(self.right)
            # self.constraint += self.left + ".begin ~ " + self.left + " .end;"
            # self.constraint += self.right + ".begin ~ " + self.right + ".end;"
        elif self.keywd == "exclude":
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp) + " = " + self.left + ".begin" + u" 🗲 " + self.right + ".begin;"
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp) + " < " + self.right + ".end;"
            ToCCSL.countTmp += 1
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp) + " = " + self.right + ".begin" + u" 🗲 " + self.left + ".begin;"
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp) + " < " + self.left + ".end;"
            ToCCSL.countTmp += 1
            ToCCSL.allState.append(self.left)
            ToCCSL.allState.append(self.right)
            # self.constraint += self.left + ".begin ~ " + self.left + ".end;"
            # self.constraint += self.right + ".begin ~ " + self.right + ".end;"
        elif self.keywd == "permit":
            ToCCSL.constraint += self.left + ".begin" + " ≤ " + self.right + ";"
            ToCCSL.constraint += self.right + " ≤ " + self.left + ".end;"
            ToCCSL.allState.append(self.left)
            ToCCSL.allEvent.append(self.right)
            # self.constraint += self.left + ".begin ~ " + self.right + ".end;"
        elif self.keywd == "forbid":
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp) + " = " + self.left + ".end" + u" 🗲 " + self.right + ";"
            ToCCSL.countTmp += 1
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp) + " = " + self.left + ".end" + u" 🗲 " + self.left + ".begin;"
            ToCCSL.countTmp += 1
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp-2) + " < " + "tmp_" + str(ToCCSL.countTmp-1) + ";"
            ToCCSL.allState.append(self.left)
            ToCCSL.allEvent.append(self.right)
        elif self.keywd == "trigger":
            if int(self.time) != 0:
                ToCCSL.constraint += self.left + " < " + self.right + ".begin;"
                ToCCSL.constraint += "0 ≤ " + self.left + " - " + self.right + ".begin" + " ≤ " + self.time + ";"
                ToCCSL.allState.append(self.right)
                ToCCSL.allEvent.append(self.left)
            else:
                ToCCSL.constraint += self.left + " == " + self.right + ".begin;"
                ToCCSL.allState.append(self.right)
                ToCCSL.allEvent.append(self.left)
        elif self.keywd == "terminate":
            if int(self.time) != 0:
                ToCCSL.constraint += self.right + ".begin" + " ≤ " + self.left + ";"
                ToCCSL.constraint += self.left + " < " + self.right + ".end;"
                ToCCSL.constraint += "0 ≤ " + self.left + " - " + self.right + ".end" + " ≤ " + self.time + ";"
                ToCCSL.allState.append(self.right)
                ToCCSL.allEvent.append(self.left)
            else:
                ToCCSL.constraint += self.left + " == " + self.right + ".end;"
                ToCCSL.allState.append(self.right)
                ToCCSL.allEvent.append(self.left)
        elif self.keywd == "within":
            ToCCSL.constraint += "0 ≤ " + "tmp_" + str(ToCCSL.countTmp) + " - " + self.left + " ≤ " + self.time + ";"
            ToCCSL.constraint += "tmp_" + str(ToCCSL.countTmp)+ " < " + self.right + ";"
            ToCCSL.countTmp += 1
            ToCCSL.allEvent.append(self.left)
            ToCCSL.allEvent.append(self.right)

    def compositeSafeNLToCCSL(self, leftList, compositeWord):
        if compositeWord == "and":
            ToCCSL.constraint += "state_" + str(ToCCSL.stateCount) +".begin" + " = " + "inf" + "("
            leftList_begin = []
            leftList_end = []
            for tmpLeft in leftList:
                leftList_begin.append(tmpLeft + ".begin")
                leftList_end.append(tmpLeft + ".end")
            strTmp = ", ".join(leftList_begin)
            ToCCSL.constraint += strTmp + ");"
            ToCCSL.constraint += "state_" + str(ToCCSL.stateCount) + ".end" + " = " + "sup" + "("
            strTmp = ", ".join(leftList_end)
            ToCCSL.constraint += strTmp + ");"
            TmpToCCSL = ToCCSL(self.keywd)
            TmpToCCSL.replaceWord("state_"+str(ToCCSL.stateCount),self.right,self.keywd)
            TmpToCCSL.safeNLToCCSL()
            ToCCSL.stateCount += 1
        elif compositeWord == "or":
            for leftTmp in leftList:
                TmpToCCSL = ToCCSL(self.keywd)
                TmpToCCSL.replaceWord(leftTmp,self.right,self.keywd)
                TmpToCCSL.safeNLToCCSL()

    @classmethod
    def AllStateAlter(cls):
        allStateSet = set(cls.allState)
        for tmpstate in allStateSet:
            cls.constraint += tmpstate + ".begin" + " ~ " + tmpstate + ".end;"

    def __str__(self):
        return "This is a class ToCCSL."

# preDef some mapping: safeNL->CCSL
imply = ToCCSL("imply")
exclude = ToCCSL("exclude")
permit = ToCCSL("permit")
forbid = ToCCSL("forbid")
trigger = ToCCSL("trigger","t1")
terminate = ToCCSL("terminate","t1")
DictCCSL = {"imply":imply,"exclude":exclude,"permit":permit,"forbid":forbid,"trigger":trigger,"terminate":terminate}

class SafeNL(object):
    def __init__(self,keywd,*args):
        self.left = "left"
        self.right = "right"
        self.keywd = keywd
        self.toCCSL = ToCCSL(keywd,*args)
        # 可以添加state,event等的属性
        if args:
            self.time = args[0]
            if self.keywd == "within":
                self.keywd_2 = args[1]
        else:
            self.time = "0"

    def replaceWord(self, left, right, keywd, *args):
        self.left = left
        self.right = right
        self.keywd = keywd
        if args:
            self.time = args[0]
            if self.keywd == "within":
                self.keywd_2 = args[1]

    def getLeft(self):
        return self.left

    def getRight(self):
        return self.right

    def getKeywd(self):
        if self.keywd == "trigger" or self.keywd == "terminate":
            return self.keywd, self.time
        elif self.keywd == "within":
            return self.keywd, self.time, self.keywd_2
        else:
            return self.keywd

    def processBasic(self):
        self.toCCSL.safeNLToCCSL()
        
    def processComposite(self):
        if self.left.find("and") != -1 and \
                self.left[self.left.find("and")-1].isspace() and \
                self.left[self.left.find("and")+3].isspace():
            leftList = re.split(r"\s+and\s+",self.left)
            for i,leftTmp in enumerate(leftList):
                leftList[i] = leftTmp.strip()
                ToCCSL.allState.append(leftList[i])
            self.toCCSL.compositeSafeNLToCCSL(leftList,"and")
        elif self.left.find("or") != -1 and \
                self.left[self.left.find("or")-1].isspace() and \
                self.left[self.left.find("or")+2].isspace():
            leftList = re.split(r"\s+or\s+",self.left)
            for i,leftTmp in enumerate(leftList):
                leftList[i] = leftTmp.strip()
                ToCCSL.allState.append(leftList[i])
            self.toCCSL.compositeSafeNLToCCSL(leftList,"or")

    def __str__(self):
        return "This is a class SafeNL."

# 重新定义自己的safeNL->CCSL，在以下地方定义：