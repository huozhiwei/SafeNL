"""
    该部分主要是用来处理那些互斥的状态(exclude)和事件(#);
    State Format : obj.attr.state
    Event Format : obj.attr.event

"""

# -*- encoding:utf-8 -*-
import re
import itertools
from Process.SafeNLToCCSL import ToCCSL

antiPrefix = ["a", "ab", "in", "im",
              "il", "ir", "un", "non",
              "de", "dis","A", "Ab",
              "In", "Im", "Il", "Ir",
              "Un", "Non", "De", "Dis"]

class ProcessSpecialStaEve(object):
    constraintToBeInStr = ""
    allStateSplitResult = []
    allEventSplitResult = []
    constraintToBeIn = []
    ExcludeStateDic = {}

    def __init__(self):
        self.SpecialStateResult()
        self.SpecialEventResult()

    @classmethod
    def AllClear(cls):
        cls.allStateSplitResult.clear()
        cls.allEventSplitResult.clear()
        cls.constraintToBeIn.clear()
        cls.ExcludeStateDic.clear()
        cls.constraintToBeInStr = ""

    def deleteSpaces(self,List):
        for i,tmp in enumerate(List):
            List[i] = tmp.strip()

    def judgeSubstrAndPre(self,str_1,str_2):
        if len(str_1) < len(str_2):
            if str_1 in str_2:
                for i,pre in enumerate(antiPrefix):
                    if str_2.startswith(pre):
                        return True
                    else: continue
                return False
            else:
                return False
        elif len(str_2) < len(str_1):
            if str_2 in str_1:
                for i,pre in enumerate(antiPrefix):
                    if str_1.startswith(pre):
                        return True
                    else: continue
                return False
            else:
                return False

    # 处理具有相同obj.attribution的state 或 event 是否互斥
    def findExclude(self,List,str_1):
        for i,tmp in enumerate(List):
            for j,tmp_1 in enumerate(List):
                if tmp[0] == tmp_1[0] and tmp[1] == tmp_1[1]:
                    if str_1 == "state" and tmp[2] != tmp_1[2]:
                        # 一键多值时用列表[]作为值,setdefault表示没有该键时设置[]为值
                         ProcessSpecialStaEve.ExcludeStateDic.setdefault\
                             (tmp[0] + "." + tmp[1], []).append(tmp[2])
                    else:
                        if self.judgeSubstrAndPre(tmp[2], tmp_1[2]):
                            if len(tmp[2]) < len(tmp_1[2]):
                                ProcessSpecialStaEve.constraintToBeIn.append \
                                (".".join(tmp) + " # " + ".".join(tmp_1))
                            else:
                                ProcessSpecialStaEve.constraintToBeIn.append \
                                (".".join(tmp_1) + " # " + ".".join(tmp))
        # 删除字典的值（List）中重复的字符串,并保持索引（index）不变
        for key,value in ProcessSpecialStaEve.ExcludeStateDic.items():
            ProcessSpecialStaEve.ExcludeStateDic[key] = sorted(set(value), key=value.index)
        # 对所有具有相同前缀的互斥状态进行组合
        for key,value in ProcessSpecialStaEve.ExcludeStateDic.items():
            # 组合List
            if len(value) >= 2:
                combinationList = list(itertools.combinations(value,2))
                for combin in combinationList:
                    ProcessSpecialStaEve.constraintToBeIn.append(
                        key + "." + combin[0] + " exclude " +
                        key + "." + combin[1])
        # 去除constraintToBeIn中的重复元素，并保持当中元素的相对位置不变
        tmpList = ProcessSpecialStaEve.constraintToBeIn
        ProcessSpecialStaEve.constraintToBeIn = sorted(set(tmpList), key=tmpList.index)
        ProcessSpecialStaEve.constraintToBeInStr = ";\n".join(ProcessSpecialStaEve.constraintToBeIn)
        ProcessSpecialStaEve.constraintToBeInStr += ";\n"

    def ProcessSpecialState(self,state):
        # stateList = ["switch", "attr", "locked"]
        # stateList = ["switch", "attr", "unlocked"]
        stateList = re.split(r"\.",state) # "."代表任何字符，需要用"\."转义
        self.deleteSpaces(stateList)
        return stateList

    def ProceSpecialEvent(self,event):
        # eventList = ["switch","command_r``eceived","locked"]
        # eventList = ["switch","command_received","unlocked"]
        eventList = re.split(r"\.",event)
        self.deleteSpaces(eventList)
        return eventList

    def SpecialStateResult(self):
        for i, state in enumerate(ToCCSL.allState):
            if len(self.ProcessSpecialState(state)) >= 3:
                self.allStateSplitResult.append(self.ProcessSpecialState(state))
        self.findExclude(self.allStateSplitResult, "state")

    def SpecialEventResult(self):
        for i,event in enumerate(ToCCSL.allEvent):
            if len(self.ProceSpecialEvent(event)) >= 3:
                self.allEventSplitResult.append(self.ProceSpecialEvent(event))
        self.findExclude(self.allEventSplitResult, "event")