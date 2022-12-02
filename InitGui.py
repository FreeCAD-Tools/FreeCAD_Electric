# -*- coding: utf-8 -*-
###############################################################################
#
#  InitGui.py
#
#  Copyright 2022 <>
#
###############################################################################
import os
import FreeCADGui

class ElectricWorkbench(FreeCADGui.Workbench):

    from TranslateUtils import translate
    from ELLocations import iconPath
    import ELCommands

    MenuText = translate("InitGui", "Electric")
    ToolTip = translate("InitGui", "Workbench for Electric")
    Icon = os.path.join(iconPath, "ElectricLogo.svg")

    def Initialize(self):
        "This function is executed when FreeCAD starts"
        cmdlist = ['ELNewSheet', 'Separator', 'ELWireMode', 'ELAddNode', 'ELAddLamp', 'ELAddButton', 'Separator', 'ELQGraphicsInit', 'ELClearBluePrint']
        self.appendToolbar("Electric Tools", cmdlist)

    def Activated(self):
        "This function is executed when the workbench is activated"
        return

    def Deactivated(self):
        "This function is executed when the workbench is deactivated"
        return

    def ContextMenu(self, recipient):
        "This is executed whenever the user right-clicks on screen"

    def GetClassName(self):
        "this function is mandatory if this is a full python workbench"
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(ElectricWorkbench())