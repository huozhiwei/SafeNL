"""
    该部分是用来处理CCSL到MyCCSL转换的，其实就是简单的CCSL语句到MyCCSL语句的mapping过程
"""

# -*- coding: utf-8 -*-
import sys
import re

allAlterCnt = 1
infBeginCnt = 1
supEndCnt = 1
boundedDiffCnt = 1
# "-"号必须在前面，不然会因先找到"<"或"≤"而找不到"-"
CCSLKeywords = ["-","<","≤","sup","inf","~","🗲","==","#","$"]
MyCCSLConsList = []

def initAll():
    global allAlterCnt,infBeginCnt,\
        supEndCnt,boundedDiffCnt
    allAlterCnt = 1
    infBeginCnt = 1
    supEndCnt = 1
    boundedDiffCnt = 1
    MyCCSLConsList.clear()

def judgeCCSLKeyword(cons):
    for keyword in CCSLKeywords:
        if cons.find(keyword) != -1:
            return keyword
        else: continue

def CCSLToMyCCSL(constraint):
    if judgeCCSLKeyword(constraint) == "<":
        tmpList = constraint.split("<")
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        strMyCCSL = "<".join(tmpList)
        strMyCCSL += ";"
        MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "≤":
        tmpList = constraint.split("≤")
        for i, tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        strMyCCSL = "≤".join(tmpList)
        strMyCCSL += ";"
        MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "sup":
        global supEndCnt
        posLbracket = constraint.index("(")
        posRbracket = constraint.index(")")
        stas = constraint[posLbracket+1:posRbracket]
        stasList = stas.split(",")
        comStaList = constraint.split("sup(")
        comSta = comStaList[0].split(".end = ")
        Sta = comSta[0]
        for i,stastmp in enumerate(stasList):
            stasList[i] = stastmp.strip()
        if len(stasList) > 2:
            strMyCCSL = Sta + "Tmp_" + str(supEndCnt) + ".end" + "=" + stasList[0] + "∨" + stasList[1] + ";"
            tmpCount = 0
            stasListCnt = 2
            while tmpCount < len(stasList) - 3:
                strMyCCSL += Sta + "Tmp_" + str(supEndCnt+1) + ".end" + "=" + Sta + "Tmp_" + str(
                    supEndCnt) + ".end" + "∨" + stasList[stasListCnt] + ";"
                supEndCnt += 1
                stasListCnt += 1
                tmpCount +=1
            strMyCCSL += Sta + ".end" + "=" + Sta + "Tmp_" + str(supEndCnt) + ".end" + "∨" + stasList[stasListCnt] + ";"
            MyCCSLConsList.append(strMyCCSL)
        else:
            strMyCCSL = Sta + ".end" + "=" + stasList[0] + "∨" + stasList[1] + ";"
            MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "inf":
        global infBeginCnt
        posLbracket = constraint.index("(")
        posRbracket = constraint.index(")")
        stas = constraint[posLbracket + 1:posRbracket]
        stasList = stas.split(", ")
        comStaList = constraint.split("inf(")
        comSta = comStaList[0].split(".begin = ")
        Sta = comSta[0]
        for i,stastmp in enumerate(stasList):
            stasList[i] = stastmp.strip()
        if len(stasList) > 2:
            strMyCCSL = Sta + "Tmp_" + str(infBeginCnt) + ".begin" + "=" + stasList[0] + "∧" + stasList[1] + ";"
            tmpCount = 0
            stasListCnt = 2
            while tmpCount < len(stasList) - 3:
                strMyCCSL += Sta + "Tmp_" + str(infBeginCnt + 1) + ".begin" + "=" + Sta + "Tmp_" + str(
                    infBeginCnt) + ".begin" + "∧" + stasList[stasListCnt] + ";"
                infBeginCnt += 1
                stasListCnt += 1
                tmpCount += 1
            strMyCCSL += Sta + ".begin" + "=" + Sta + "Tmp_" + str(infBeginCnt) + ".begin" + "∧" + stasList[stasListCnt] + ";"
            MyCCSLConsList.append(strMyCCSL)
        else:
            strMyCCSL = Sta + ".begin" + "=" + stasList[0] + "∧" + stasList[1] + ";"
            MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "~":
        global allAlterCnt
        tmpList = constraint.split("~")
        for i, tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        strMyCCSL = tmpList[0] + "<" + tmpList[1] + ";"
        strMyCCSL += "tmpState_" + str(allAlterCnt) + "=" + tmpList[0] +"$1" + ";"
        strMyCCSL += tmpList[1] + "<" + "tmpState_" + str(allAlterCnt) + ";"
        allAlterCnt += 1
        MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == u"🗲": # sampleOn
        tmpList = constraint.split(u"🗲")
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        leftTmpList = tmpList[0].split("=")
        for i,leftTmp in enumerate(leftTmpList):
            leftTmpList[i] = leftTmp.strip()
        leftTmpStr = "=".join(leftTmpList)
        strMyCCSL = leftTmpStr + "☇" + tmpList[1] + ";"
        MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "==": # two events conincidence
        tmpList = constraint.split("==")
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        strMyCCSL = "==".join(tmpList)
        strMyCCSL += ";"
        MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "-": # boundedDiff
        # "0 ≤ C1 - C2 ≤ t1"
        global boundedDiffCnt
        constraintList = constraint.split()
        time = constraintList[-1]
        strMyCCSL = constraintList[2] + "≤" + constraintList[4] + ";"
        strMyCCSL += "Tmp_" + str(boundedDiffCnt) + "=" + constraintList[2] + "$" + \
                     str(round(float(time)/10)) + " on idealClcok" + ";"
        strMyCCSL += constraintList[4] + "≤" + "Tmp_" + str(boundedDiffCnt) + ";"
        boundedDiffCnt += 1
        MyCCSLConsList.append(strMyCCSL)

    elif judgeCCSLKeyword(constraint) == "#": # two events exclude
        tmpList = constraint.split("#")
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        strMyCCSL = "#".join(tmpList)
        strMyCCSL += ";"
        MyCCSLConsList.append(strMyCCSL)

    else: #  处理带"$"符号的CCSL语句
        tmpList = constraint.split()
        for i,tmp in enumerate(tmpList):
            tmpList[i] = tmp.strip()
        delay = tmpList[tmpList.index("=") + 2][1:]
        delaytime = str(round(float(delay)/10))
        tmpList_1 = constraint.split("$")
        for i,tmp in enumerate(tmpList_1):
            tmpList_1[i] = tmp.strip()
        if tmpList_1[1].isdigit():
            strMyCCSL = tmpList_1[0] + " $" + delaytime
        else:
            tmpstr = " ".join(tmpList[tmpList.index("=") + 3:])
            strMyCCSL = tmpList_1[0] + " $" + delaytime + tmpstr
        strMyCCSL += ";"
        MyCCSLConsList.append(strMyCCSL)

# 之后将MyCCSLConsList写文件
