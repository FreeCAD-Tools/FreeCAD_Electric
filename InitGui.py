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
import PySide

class ElectricWorkbench(FreeCADGui.Workbench):

    from ELLocations import getIconPath

    MenuText = "Electric"
    ToolTip = "Workbench for Electric"
    Icon = getIconPath("ElectricLogo.svg")

    def Initialize(self):
        import ELCommands, ELSymbolCommands, ELTechDrawCommands
    
        "This function is executed when FreeCAD starts"
        cmdlist = ELTechDrawCommands.CommandList
        self.appendToolbar("TechDraw Electric Commands", cmdlist)
        cmdlist = ELTechDrawCommands.SymbolCommandList
        self.appendToolbar("TechDraw Electric Symbols", cmdlist)
        
        cmdlist = ELCommands.CommandList
        self.appendToolbar("Electric BluePrint Commands", cmdlist)
        cmdlist = ELSymbolCommands.SymbolCommandList
        self.appendToolbar("Electric BluePrint Symbols", cmdlist)

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

print ("QtCore Version: ",PySide.QtCore.qVersion())

FreeCADGui.addWorkbench(ElectricWorkbench())

class SelObserver:
    def onSelectionChanged(self,doc,obj,sub,pnt):
        App.Console.PrintMessage("onSelectionChanged "+str(doc)+","+str(obj)+","+str(sub)+","+str(pnt)+" \n")
    def addSelection(self,doc,obj,sub,pnt):
        App.Console.PrintMessage("addSelection "+str(doc)+","+str(obj)+","+str(sub)+","+str(pnt)+" \n")
        if App.getDocument(str(doc)).getObject(str(obj)).Visibility == False:
            App.getDocument(str(doc)).getObject(str(obj)).Visibility = True
    def removeSelection(self,doc,obj,sub):
        App.Console.PrintMessage("removeSelection "+str(doc)+","+str(obj)+","+str(sub)+" \n")
        #obj = App.getDocument(doc).getObject(obj)
        #if hasattr(obj, "BluePrintElementType"):
        #    print ("remove ",obj)
        #    obj.Proxy.onDelete()
        #else:
        #    print ("no attrib")        
    def setSelection(self,doc,obj,sub,pnt):
        App.Console.PrintMessage("setSelection "+str(doc)+","+str(obj)+","+str(sub)+","+str(pnt)+" \n")        
    def clearSelection(self,doc):
        print ("clearSelection")
    def setPreselection(self,doc,obj,sub):
        App.Console.PrintMessage("setPreselection "+str(doc)+","+str(obj)+","+str(sub)+" \n") 
    def removePreselection(self,doc,obj,sub):
        App.Console.PrintMessage("removePreselection "+str(doc)+","+str(obj)+","+str(sub)+" \n") 
        #if hasattr(obj, "BluePrintElementType"):
        #    print ("remove ",obj)
        #    obj.Proxy.onDelete()
    def pickedListChanged():
        App.Console.PrintMessage("pickedListChanged \n") 

s=SelObserver()
FreeCADGui.Selection.addObserver(s)