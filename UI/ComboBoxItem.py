# -*- encoding:utf-8 -*-

# "within" 必须在 "forbid"前
safenlKw = ["within","imply","exclude","permit","trigger","terminate","forbid"]
CCSLKw = ["<","≤","sup","inf","~","🗲","==","-","#","$"]

def setSafeNLCb():
    return safenlKw

def setCCSLCb():
    return CCSLKw