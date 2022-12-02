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
import BluePrint
from PySide import QtGui, QtCore, QtSvg

def getIconPath(file):
   return os.path.join(iconPath, file)
   
def getSymbolPath(file):
   return os.path.join(symbolsPath, file)

CommandList = []   

def addCommand(name, function = None):
    CommandList.append(name)
    if function is not None:
        Gui.addCommand(name, function)

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
        scene = self.createTestScene()
        view = QtGui.QGraphicsView() #BluePrint.GraphicsView() #QtGui.QGraphicsView()
        view.setBackgroundBrush(QtGui.Qt.gray)
        view.setScene(scene)
        view.setMouseTracking(True)
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
        svg = QtSvg.QGraphicsSvgItem(getSymbolPath('Lamp.svg'))
        scene.svg1 = scene.addItem(svg) 
        svg.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        svg.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        
        # https://stackoverflow.com/questions/56259690/qt-moving-a-qgraphicsitem-causes-artifacts-leaves-trailes-behind
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

addCommand('ELQGraphicsInit', ELQGraphicsInit())

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


