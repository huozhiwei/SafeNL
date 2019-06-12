# -*- encoding:utf-8 -*-
from Process.CCSLToMyCCSL import CCSLToMyCCSL

def ProcessCCSL(inputMyCCSLstr):
    # 传入的每条CCSL元素包含着用";"隔开的各种MyCCSL语句
    tmpList = inputMyCCSLstr.split(";")
    text = ""
    for i,tmpstr in enumerate(tmpList):
        tmpList[i] = tmpstr.strip()
    for i,tmpstr in enumerate(tmpList):
        if tmpstr and not tmpstr.isspace():
            text = text + tmpstr + "\n"
    return text

