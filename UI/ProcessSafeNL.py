# -*- encoding:utf-8 -*-
import re
from Process.SafeNLToCCSL import SafeNL,ToCCSL

# "within" 必须在 "forbid"前
safenlKw = ["within","imply","exclude","permit","trigger","terminate","forbid"]
# "-"号必须在前面，不然会因先找到"<"或"≤"而找不到"-"
CCSLKw = ["-","<","≤","sup","inf","~", u"🗲", "==", "#", "$"]

class ProcessSafeNL(object):
    def __init__(self,SafeNLstr):
        self.SafeNLstr = SafeNLstr
        self.SafeNLlist = self.__processstr(SafeNLstr)
        self.SafeNLlist = self.SafeNLlist[1:]
        # 去除重复SafeNL语句并保持当中元素相对位置不变
        SafeNLlist = self.SafeNLlist
        # 返回值是一个列表
        self.SafeNLlist = sorted(set(SafeNLlist), key=SafeNLlist.index)
        # 每一个元素都是SafeNL对象
        self.safenlToCCSL = []
        # self.splitSafeNLKw(safenltmp) = (tmpkwList,safenlkw,time,safenlkw_2)
        # 其中time,safenlkw_2 在safenlkw = "within" 才有，time在safenlkw = "trigger"
        # 和safenlkw = "terminate" 才有
        self.generateSafeNLSplitList()
        self.generateCCSLConstrans()

    def __processstr(self,proc_str):
        tmpList = proc_str.split(";")
        # 处理每个元素两边的空格
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        tmpexList = []
        # 将空字符串和纯空格字符串去掉
        for tmp in tmpList:
            if tmp and not tmp.isspace():
                tmpexList.append(tmp)
        tmpList = tmpexList
        return tmpList

    def checkIfeventsCCSL(self,safenltmp):
        for i,ccslkw in enumerate(CCSLKw):
            if ccslkw in safenltmp:
                print(ccslkw,"5")
                return True
        return False

    def splitSafeNLKw(self,safenltmp):
        for i,safenlkw in enumerate(safenlKw):
            if safenlkw in safenltmp:
                if safenlkw == "trigger" \
                or safenlkw == "terminate":
                    tmpList = safenltmp.split()
                    if "in" in tmpList:
                        time = tmpList[tmpList.index("in") + 1]
                        # tmpkwList = [left,right]
                        tmpkwList = re.split(r"\s+" + safenlkw + r"\s+",safenltmp)
                        # 改变right为"obj.attr.state"，否则为"obj.attr.state in 30 ms"
                        tmpkwList[-1] = tmpList[tmpList.index("in") - 1]
                        for i,tmpkw in enumerate(tmpkwList):
                            tmpkwList[i] = tmpkw.strip()
                    else:
                        time = "0"
                        # tmpkwList = [left,right]
                        tmpkwList = re.split(r"\s+" + safenlkw + r"\s+",safenltmp)
                        for i,tmpkw in enumerate(tmpkwList):
                            tmpkwList[i] = tmpkw.strip()
                    return tmpkwList,safenlkw,time
                elif safenlkw == "within":
                    tmpList = safenltmp.split()
                    # time 在safeNL中是这种形式:[0,30]ms
                    timewithextra = tmpList[tmpList.index("within") + 1]
                    time = timewithextra[timewithextra.find(",")+1:timewithextra.find("]")].strip()
                    safenlkw_2 = tmpList[tmpList.index("within") + 2]
                    tmpkwList = re.split(r"\s+" + safenlkw + r"\s+",safenltmp)
                    # 改变right为"obj2.attr2.event2",否则为"[0,30]ms forbid obj2.attr2.event2"
                    tmpkwList[-1] = tmpList[-1]
                    for i,tmpkw in enumerate(tmpkwList):
                        tmpkwList[i] = tmpkw.strip()
                    return tmpkwList,safenlkw,time,safenlkw_2
                else:
                    tmpkwList = re.split(r"\s+" + safenlkw + r"\s+",safenltmp)
                    for i,tmpkw in enumerate(tmpkwList):
                        tmpkwList[i] = tmpkw.strip()
                    return tmpkwList,safenlkw

    def generateSafeNLSplitList(self):
        # self.splitSafeNLKw(safenltmp) = (tmpkwList,safenlkw,time,safenlkw_2)
        # 其中time,safenlkw_2 在safenlkw = "within" 才有，time在safenlkw = "trigger"
        # 和safenlkw = "terminate" 才有
        for safenltmp in self.SafeNLlist:
            if self.checkIfeventsCCSL(safenltmp):
                print(safenltmp,"4")
                ToCCSL.constraint += safenltmp + ";"
                # if "sup" in safenltmp \
                # or "inf" in safenltmp:
                #     splitList = re.split(r"\s+sup|inf\S+",safenltmp)
                #     rightStr = splitList[1]
                #     posLbracket = rightStr.find("(")
                #     posRbracket = rightStr.find(")")
                #     stas = rightStr[posLbracket + 1:posRbracket]
                #     stasList = stas.split(", ")
                #     for i,stastmp in enumerate(stasList):
                #         stasList[i] = stastmp.strip()
                #         ToCCSL.allState.append(stasList[i])
            else:
                tmptuple = self.splitSafeNLKw(safenltmp)
                if tmptuple[1] == "trigger" \
                    or tmptuple[1] == "terminate":
                    tmpSafeNL = SafeNL(tmptuple[1],tmptuple[2])
                    tmpSafeNL.replaceWord(tmptuple[0][0],tmptuple[0][1],tmptuple[1],tmptuple[2])
                    tmpSafeNL.toCCSL.replaceWord(tmptuple[0][0],tmptuple[0][1],tmptuple[1],tmptuple[2])
                    self.safenlToCCSL.append(tmpSafeNL)
                elif tmptuple[1] == "within":
                    tmpSafeNL = SafeNL(tmptuple[1],tmptuple[2],tmptuple[3])
                    tmpSafeNL.replaceWord(tmptuple[0][0], tmptuple[0][1], tmptuple[1], tmptuple[2],tmptuple[3])
                    tmpSafeNL.toCCSL.replaceWord(tmptuple[0][0], tmptuple[0][1], tmptuple[1], tmptuple[2],tmptuple[3])
                    self.safenlToCCSL.append(tmpSafeNL)
                else:
                    tmpSafeNL = SafeNL(tmptuple[1])
                    tmpSafeNL.replaceWord(tmptuple[0][0], tmptuple[0][1], tmptuple[1])
                    tmpSafeNL.toCCSL.replaceWord(tmptuple[0][0], tmptuple[0][1], tmptuple[1])
                    self.safenlToCCSL.append(tmpSafeNL)

    def generateCCSLConstrans(self):
        for i,safenlele in enumerate(self.safenlToCCSL):
            if re.search(r"\s+and\s+",safenlele.left) == None \
                and re.search(r"\s+or\s+",safenlele.left) == None:
                self.safenlToCCSL[i].processBasic()
            else:
                self.safenlToCCSL[i].processComposite()
        ToCCSL.AllStateAlter()

