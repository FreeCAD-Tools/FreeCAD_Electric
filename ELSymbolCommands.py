# -*- coding: utf-8 -*-
###############################################################################
#
#  ELSymbolCommands.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################

from FreeCAD import Gui
from FreeCAD import Base
import FreeCAD
import FreeCAD as App      # !!!
import FreeCADGui
import os
import math
import random
from ELLocations import getIconPath, getSymbolPath, getTemplatePath
from PySide import QtGui, QtCore, QtSvg
import Features.BPSymbolFeature as Symbol

# this list must be getted from symbols folder
SymbolList = {
    # (key) type : short label
    "Node" : "N",
    "Lamp" : "HL",
    "Button" : "SB",
    "RelayCoil" : "KM",
    "RelayContact" : "K",
}

SymbolCommandList = []

class SymbolCommand:
    """Add Symbol command"""

    def __init__(self, type, help):
        self.Type = type
        self.Code = help

    def GetResources(self):
        
        return {'Pixmap': getIconPath('EL' + self.Type + '.svg'),
                'MenuText': "Add "+self.Type+" symbol",
                'ToolTip': "Add "+self.Code}

    def TryToGetBluePrintFromActiveTab(self):
        activeSubWindow = FreeCADGui.getMainWindow().findChild(QtGui.QMdiArea).activeSubWindow()
        if activeSubWindow.__class__.__name__ == 'MDIViewBluePrint':
            return activeSubWindow.obj
        return None            

    def Activated(self):
        bp = self.TryToGetBluePrintFromActiveTab()
        if bp is not None:
            Symbol.Create(bp, self.Type, random.randint(200,400), random.randint(200,400))
            App.ActiveDocument.recompute()
        return

    def IsActive(self):
        return self.TryToGetBluePrintFromActiveTab() is not None 
        #str(FreeCADGui.Selection.getSelectionEx()[0].Object.Proxy.__class__) == "<class 'Features.BluePrintFeature.BluePrintFeature'>" #Gui.ActiveDocument is not None

def AddSymbolCommand(type):
    cmd = 'EL' + type
    Gui.addCommand(cmd, SymbolCommand(type,SymbolList[type]))   # Add command to FreeCAD Envorinment
    SymbolCommandList.append(cmd)                       # Add command to list of Symbols toolbar

# generate all commands
for key in SymbolList:
    AddSymbolCommand(key)