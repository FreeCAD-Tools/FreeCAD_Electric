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
import BluePrint
from PySide import QtGui, QtCore

def getIconPath(file):
   return os.path.join(iconPath, file)
   
def getSymbolsPath(file):
   return os.path.join(symbolsPath, file)

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
        zf = zipfile.ZipFile(getSymbolsPath('GOST.zip'),'r')
        icon = zf.read('Lamp.svg')
        zf.close()
        print(icon)
        return

    def IsActive(self):
        return Gui.ActiveDocument is not None

Gui.addCommand('ELZipTest', ELZipTest())

scene = BluePrint.GraphicsScene()

class ELQGraphicsInit:
    """QGraphicsInit"""

    def GetResources(self):
        return {
            'Pixmap': getIconPath('ELNewBluePrint.svg'),
            'MenuText': "Create New Blue Print",
            'ToolTip': "Test of GraphicsScene"
        }

    def Activated(self):
        #blueprint.show()
        scene = self.createTestScene()
        view = QtGui.QGraphicsView() #BluePrint.GraphicsView() #QtGui.QGraphicsView()
        view.setBackgroundBrush(QtGui.Qt.gray)
        view.setScene(scene)
        self.addMDIView(view,'BluePrint')
        return

    def createTestScene(self):
        '''create test scene'''
        scene = BluePrint.GraphicsScene() #QtGui.QGraphicsScene()
        framecolor = QtGui.QPen(QtGui.Qt.black)
        backcolor = QtGui.QBrush(QtGui.Qt.white)
        scene.rect = scene.addRect(-400,-400,800,600,framecolor,backcolor)
        scene.line1 = scene.addLine(-10,-115,90,-116)
        scene.ellipse = scene.addEllipse(20,20,100,50)
        pen = QtGui.QPen(QtGui.Qt.red)
        scene.rect = scene.addRect(-20,-20,40,40,pen)
        scene.rect.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        scene.line2 = scene.addLine(0,0,50,50)
        scene.line2.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        font = QtGui.QFont("Arial", 16, 2, False)
        scene.text = scene.addText('HL1', font)
        return scene


    def addMDIView(self,view,tabText):
        '''add new MDIView and set tab text'''
        mainWindow = FreeCADGui.getMainWindow()
        mdiArea = mainWindow.findChild(QtGui.QMdiArea)
        subWindow = mdiArea.addSubWindow(view)
        subWindow.show()
        mdiArea.setActiveSubWindow(subWindow)
        tab = mainWindow.findChildren(QtGui.QTabBar)[0]
        tab.setTabText(tab.count()-1,tabText)

    def IsActive(self):
        return True #Gui.ActiveDocument is not None

Gui.addCommand('ELQGraphicsInit', ELQGraphicsInit())

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

Gui.addCommand('ELClearBluePrint', ELClearBluePrint())


