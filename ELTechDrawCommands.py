# -*- coding: utf-8 -*-
###############################################################################
#
#  ELTechDrawCommands.py
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

CommandList = []   

def addCommand(name, function = None):
    CommandList.append(name)
    if function is not None:
        Gui.addCommand(name, function)

class ELWireMode:
    """Switch to wire mode"""
    
    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELWireMode.svg'),
            'MenuText': "Switch to wire edit mode",
            'ToolTip': "Switch to wire edit mode"
        }

    def Activated(self):
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

addCommand('ELWireMode', ELWireMode())

class ELNewSheet:
    """Add new sheet"""
    
    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELNewSheet.svg'),
            'MenuText': "Add new TechDraw sheet",
            'ToolTip': "Add new TechDraw sheet"
        }

    def Activated(self):
        page = FreeCAD.activeDocument().addObject('TechDraw::DrawPage','Page')
        template = FreeCAD.activeDocument().addObject('TechDraw::DrawSVGTemplate','Template')
        template.Template = getTemplatePath('Default.svg')
        page.Template = template
        Gui.Selection.addSelection(page)
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

addCommand('ELNewSheet', ELNewSheet())

addCommand('Separator')

class ELZipTest:
    """Zip test"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELZipTest.svg'),
            'MenuText': "Zip test",
            'ToolTip': "Zip Test"
        }

    def Activated(self):
        import zipfile
        import io
        zf = zipfile.ZipFile(getSymbolPath('GOST.zip'),'r')
        icon = zf.read('Lamp.svg')
        zf.close()
        print(icon)
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

addCommand('ELZipTest', ELZipTest())

# ---------------------------------------------------------------------------------------

def addSymbol(file,code):
    f = open(getSymbolPath(file),'r')
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
        return Gui.Selection.getSelectionEx()[0].Object.TypeId ==  'TechDraw::DrawPage' #Gui.ActiveDocument is not None

def AddSymbolCommand(type):
    cmd = 'ELTD' + type
    Gui.addCommand(cmd, SymbolCommand(type,SymbolList[type]))   # Add command to FreeCAD Envorinment
    SymbolCommandList.append(cmd)                       # Add command to list of Symbols toolbar

# generate all commands
for key in SymbolList:
    AddSymbolCommand(key)