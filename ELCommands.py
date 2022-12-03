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
from ELLocations import getIconPath, getSymbolPath
from PySide import QtGui, QtCore, QtSvg
from Features.BluePrintFeature import CreateBluePrintFeature, BluePrintFeature, BluePrintViewProvider

CommandList = []   

def addCommand(name, function = None):
    CommandList.append(name)
    if function is not None:
        Gui.addCommand(name, function)

class ELCreateFeature:
    """CreateFeature"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELNewBluePrint.svg'),
            'MenuText': "CreateFeature",
            'ToolTip': "CreateFeature"
        }

    def Activated(self):
        CreateBluePrintFeature()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

addCommand('ELCreateFeature', ELCreateFeature())

class ELClearBluePrint:
    """QGraphicsInit"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELClearScene.svg'),
            'MenuText': "Clear scene",
            'ToolTip': "Remove all lines"
        }

    def Activated(self):
        scene.clear()
        return

    def IsActive(self):
        return True #Gui.ActiveDocument is not None

addCommand('ELClearBluePrint', ELClearBluePrint())
