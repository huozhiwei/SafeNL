# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *

from PyQt5.QtCore import pyqtSignal

def setStepText():
    text = "<font color='black' size=5><b>Operation steps:</b></font> <br> <br>"
    text = text + "<font color='black' size=4><i>1、Import a SafeNL Doc.</i></font> <br>"
    text = text + "<font color='black' size=4><i>2、Input some external constraints using SafeNL or CCSL.</i></font> <br>"
    text = text + "<font color='black' size=4><i>3、Push the button 'SafeNL->CCSL'.</i></font> <br>"
    text = text + "<font color='black' size=4><i>4、Push the button 'CCSL->MyCCSL'.<i></font> <br>"

    return text

