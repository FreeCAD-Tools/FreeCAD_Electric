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
import FreeCADGui
import os
import math
from ELLocations import iconPath

class ELWireMode:
    """Switch to wire mode"""
    
    def GetResources(self):
        icon = os.path.join(iconPath, 'ELWireMode.svg')
        return {
            'Pixmap': icon,
            'MenuText': "Switch to wire mode",
            'ToolTip': "Switch to wire mode"
        }

    def Activated(self):
        # Actions
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELWireMode', ELWireMode())

class ELNewSheet:
    """Add new sheet"""
    
    def GetResources(self):
        icon = os.path.join(iconPath, 'ELNewSheet.svg')
        return {
            'Pixmap': icon,
            'MenuText': "Add new sheet",
            'ToolTip': "Add new sheet"
        }

    def Activated(self):
        # Actions
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELNewSheet', ELNewSheet())

class ELAddLamp:
    """Add lamp symbol"""

    def GetResources(self):
        icon = os.path.join(iconPath, 'ELAddLamp.svg')
        return {
            'Pixmap': icon,
            'MenuText': "Add lamp",
            'ToolTip': "Add lamp"
        }

    def Activated(self):
        # Actions
        FreeCAD.ActiveDocument.recompute()
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELAddLamp', ELAddLamp())