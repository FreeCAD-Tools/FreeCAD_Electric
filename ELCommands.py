# -*- coding: utf-8 -*-
###############################################################################
#
#  ELCommands.py
#
#  Copyright 2022 <>
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

Gui.addCommand('ELWireMode', ELWireMode())

class ELNewSheet:
    """Add new sheet"""
    
    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELNewSheet.svg'),
            'MenuText': "Add new sheet",
            'ToolTip': "Add new sheet"
        }

    def Activated(self):
        page = FreeCAD.activeDocument().addObject('TechDraw::DrawPage','Page')
        template = FreeCAD.activeDocument().addObject('TechDraw::DrawSVGTemplate','Template')
        template.Template = os.path.join(templatesPath, 'Default.svg')
        page.Template = template
        Gui.Selection.addSelection(page)
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELNewSheet', ELNewSheet())

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

class ELAddNode:
    """Add Node symbol"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELNode.svg'),
            'MenuText': "Add Node",
            'ToolTip': "Add Node symbol to a draft"
        }

    def Activated(self):
        addSymbol('Node.svg','N')
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELAddNode', ELAddNode())

class ELAddLamp:
    """Add lamp symbol"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELLamp.svg'),
            'MenuText': "Add Lamp",
            'ToolTip': "Add Lamp symbol to a draft"
        }

    def Activated(self):
        addSymbol('Lamp.svg','HL')
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELAddLamp', ELAddLamp())

class ELAddButton:
    """Add button symbol"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELButton.svg'),
            'MenuText': "Add Button",
            'ToolTip': "Add Button symbol to a draft"
        }

    def Activated(self):
        addSymbol('Button.svg','SB')
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELAddButton', ELAddButton())


