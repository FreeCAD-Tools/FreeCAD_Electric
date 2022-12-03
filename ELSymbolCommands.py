# -*- coding: utf-8 -*-
###############################################################################
#
#  ELCommands.py
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
from ELLocations import iconPath, templatesPath, symbolsPath

def getIconPath(file):
   return os.path.join(iconPath, file)
   
def getSymbolPath(file):
   return os.path.join(symbolsPath, file)

def addSymbol(file,code):
    f = open(os.path.join(symbolsPath, file),'r')
    svg = f.read()
    f.close()
    symbol = FreeCAD.activeDocument().addObject('TechDraw::DrawViewSymbol',code)
    symbol.Symbol = svg
    symbol.Label = symbol.Label.replace(code+"00",code)  # !!!
    #symbol.Caption = "Caption"
    selectedObjects = FreeCADGui.Selection.getSelection()
    page = selectedObjects[0]        
    page.addView(symbol)
    FreeCAD.ActiveDocument.recompute()

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
        addSymbol(self.Type+'.svg',self.Code)
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

def AddSymbolCommand(type):
    cmd = 'EL' + type
    Gui.addCommand(cmd, SymbolCommand(type,SymbolList[type]))   # Add command to FreeCAD Envorinment
    SymbolCommandList.append(cmd)                       # Add command to list of Symbols toolbar

# generate all commands
for key in SymbolList:
    AddSymbolCommand(key)