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
from ELLocations import getIconPath, getSymbolPath, getTemplatePath

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

    def Activated(self):
        '''for selObj in ELBase.GetAttachableSelections():
            a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", self.TypeName)
            ScrewObject(a, self.Type, selObj)
            a.Label = a.Proxy.familyType
            FSViewProviderTree(a.ViewObject)
        FreeCAD.ActiveDocument.recompute()'''
        #addSymbol(self.Type+'.svg',self.Code)
        # Get name of selected object
        obj = FreeCADGui.Selection.getSelectionEx()[0].Object
        print(obj.Name)
        # if object is BluePrintFeature
        obj.Proxy.addShape(self.Type)
        return

    def IsActive(self):
        return str(FreeCADGui.Selection.getSelectionEx()[0].Object.Proxy.__class__) == "<class 'Features.BluePrintFeature.BluePrintFeature'>" #Gui.ActiveDocument is not None

def AddSymbolCommand(type):
    cmd = 'EL' + type
    Gui.addCommand(cmd, SymbolCommand(type,SymbolList[type]))   # Add command to FreeCAD Envorinment
    SymbolCommandList.append(cmd)                       # Add command to list of Symbols toolbar

# generate all commands
for key in SymbolList:
    AddSymbolCommand(key)