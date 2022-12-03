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
from ELLocations import getIconPath, getSymbolPath, getTemplatePath
from PySide import QtGui, QtCore, QtSvg
from Features.BluePrintFeature import CreateBluePrintFeature, BluePrintFeature, BluePrintViewProvider
from Features.BPSymbolFeature import CreateBPSymbolFeature, BPSymbolFeature, BPSymbolViewProvider

CommandList = []   

def addCommand(name, function = None):
    CommandList.append(name)
    if function is not None:
        Gui.addCommand(name, function)

class ELAddBluePrintSheet:
    """AddBluePrintSheet"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELNewBluePrint.svg'),
            'MenuText': "Add a new BluePrint sheet",
            'ToolTip': "Add a new BluePrint sheet"
        }

    def Activated(self):
        if FreeCAD.ActiveDocument == None:
            FreeCAD.newDocument()
        bp = CreateBluePrintFeature()
        bp.Template = getTemplatePath('Default.svg')
        bp.Proxy.addShape('Lamp')
        bp.Proxy.addShape('Button',400,250)
        bp.Proxy.addShape('RelayCoil',300,400)
        bp.Proxy.addLabel('Text Label',200,200)
        # Recompute document (object)
        App.ActiveDocument.recompute()  # Mandatory! After change properties of object.
        # Select created object
        Gui.Selection.addSelection(bp)
        return

    def IsActive(self):
        return True   #return Gui.ActiveDocument is not None

addCommand('ELAddBluePrintSheet', ELAddBluePrintSheet())

class ELAddLamp:

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELLamp.svg'),
            'MenuText': "Add lamp svg item",
            'ToolTip': "Add lamp svg item"
        }

    def Activated(self):
        # Get name of selected object
        bps = CreateBPSymbolFeature()
        App.ActiveDocument.recompute()
        Gui.Selection.addSelection(bps)
        return

    def IsActive(self):
        return str(FreeCADGui.Selection.getSelectionEx()[0].Object.Proxy.__class__) == "<class 'Features.BluePrintFeature.BluePrintFeature'>" #Gui.ActiveDocument is not None

addCommand('ELAddLamp', ELAddLamp())
