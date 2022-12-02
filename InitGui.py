# -*- coding: utf-8 -*-
###############################################################################
#
#  InitGui.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
import os
import FreeCADGui

class ElectricWorkbench(FreeCADGui.Workbench):

    from ELLocations import iconPath

    MenuText = "Electric"
    ToolTip = "Workbench for Electric"
    Icon = os.path.join(iconPath, "ElectricLogo.svg")

    def Initialize(self):
        import ELCommands, ELSymbolCommands, ELTechDrawCommands
    
        "This function is executed when FreeCAD starts"
        cmdlist = ELTechDrawCommands.CommandList
        self.appendToolbar("TechDraw Electric Commands", cmdlist)
        cmdlist = ELTechDrawCommands.SymbolCommandList
        self.appendToolbar("TechDraw Electric Symbols", cmdlist)
        
        cmdlist = ELCommands.CommandList
        self.appendToolbar("Electric BluePrint Commands", cmdlist)

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
