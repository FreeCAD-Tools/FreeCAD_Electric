# -*- coding: utf-8 -*-
###############################################################################
#
#  SymbolFeature.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
from FreeCAD import Gui
import FreeCAD as App
import FreeCADGui
import os
from PySide import QtGui, QtCore, QtSvg
from ELLocations import getIconPath, getSymbolPath

def CreateBPSymbolFeature(page, name, x, y):
    obj = App.ActiveDocument.addObject('App::FeaturePython', name)
    
    renderer = QtSvg.QSvgRenderer()
    svg = SymbolItem(obj, page)
    svg.setSharedRenderer(renderer)
    svg.renderer().load(getSymbolPath(name+".svg"))   # The problem is that when using the QSvgRenderer to load the .svg then 
                                    # the boundingRect of the QGraphicsSvgItem is not updated so nothing will be drawn
    svg.setElementId("")       # Solution is to use passing an empty string to the setElementId method to recalculate bounding box

    svg.setCursor(QtCore.Qt.SizeAllCursor)
    svg.setToolTip("This object is signal lamp it turned on after user press the gren button. It shows than pump motor is start to working.")
    #svg.setRotation(45) # Почему-то при повороте выводится все изображение
    #svg.setParentItem(parentItem) # For move grouping
    
    item = page.scene.addItem(svg) 
    svg.setPos(x, y)
    svg.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
    svg.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
    svg.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
    svg.setElementId("")
    
    BPSymbolFeature(obj, page, svg)
    BPSymbolViewProvider(obj.ViewObject)
    obj.X = x
    obj.Y = y
    
    return obj

class SymbolItem(QtSvg.QGraphicsSvgItem):
    
    def __init__(self, obj, page):
        super().__init__()
        self.obj = obj
        self.page = page

    def itemChange(self, change, value):
        print(change)
        if change == self.ItemPositionChange:
            value = QtCore.QPointF(value.x() // 10 * 10, value.y() // 10 * 10)
            #self.obj.X = value.x()
            #self.obj.Y = value.y()
            #self.obj.recompute()
            #return value
            #self.setPos(value.x() // 10 * 10, value.y() // 10 * 10)
        if change == self.ItemSelectedChange:
            if value == True:
                #Gui.Selection.clearSelection()
                Gui.Selection.addSelection(self.obj)
            else:
                Gui.Selection.removeSelection(self.obj)                
        return super().itemChange(change, value)

    def mouseReleaseEvent(self, event):
        print("symbol mrel event", event)
        super().mouseReleaseEvent(event)
        self.obj.X = self.x()
        self.obj.Y = self.y()
#        self.page.recompute()
        App.ActiveDocument.recompute()

# item должна быть внутри Feature
class BPSymbolFeature():

    def __init__(self, obj, bpf, item):
        App.Console.PrintMessage("BPSymbolFeature init object \n")
        self.Type = 'BPSymbolFeature'
        obj.addProperty('App::PropertyString', 'Description', 'Base', 'Feature description').Description = ""
        obj.addProperty('App::PropertyString', 'BluePrintElementType', 'Data', 'This is Id for Workbench').BluePrintElementType = "Symbol"
        obj.addProperty('App::PropertyString', 'ElementId', 'Data', 'ElementId in QGraphicsScene').ElementId = "?"
        obj.addProperty('App::PropertyFloat', 'X', 'Position', 'X position on sheet').X = 50.0
        obj.addProperty('App::PropertyFloat', 'Y', 'Position', 'Y position on sheet').Y = 50.0
        obj.Proxy = self
        self.bpf = bpf
        self.item = item
        self.obj = obj

    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        App.Console.PrintMessage("BPSymbolFeature Change property: " + str(prop) + "\n")
        val = obj.getPropertyByName(prop)
        #if item with elemntid in scene not exist add item to scene
        #if prop == "X":
        #    self.obj.X = self.x()
        #    App.ActiveDocument.recompute()
        #if prop == "Y":
        #    self.obj.Y = self.y()
        #    App.ActiveDocument.recompute()
        #if prop == "Visibility":
        #    if val == True:
        #        self.createTabIfItNotExists(obj)   # Needs to open mdi tab again
        #    else:
        #        self.frame.close()            

    def onDelete(self):
        App.Console.PrintMessage("BPSymbolFeature onDelete \n")
        print(self.item)
        self.bpf.scene.removeItem(self.item)

    def onDocumentRestored(self, obj):
        App.Console.PrintMessage("BPSymbolFeature onDocumentRestored " + str(obj) + " \n")

    def execute(self, obj):
        App.Console.PrintMessage("BPSymbolFeature execute \n")  

class BPSymbolViewProvider:

    def __init__(self, obj):
        """ Set this object to the proxy object of the actual view provider """
        obj.Proxy = self

    def attach(self, obj):
        from pivy import coin    # Without that icon is be gray        
        """ Setup the scene sub-graph of the view provider, this method is mandatory """
        App.Console.PrintMessage("BPSymbolViewProvider attach \n")
        self.standard = coin.SoGroup()
        obj.addDisplayMode(self.standard,"Standard");
        return

    def updateData(self, obj, prop):
        """ If a property of the handled feature has changed we have the chance to handle this here """
        App.Console.PrintMessage("BPSymbolViewProvider updateData \n")
        return

    def getDisplayModes(self, obj):
        """ Return a list of display modes. """
        App.Console.PrintMessage("BPSymbolViewProvider getDisplayModes \n")
        return ["Standard"]

    def getDefaultDisplayMode(self):
        """ Return the name of the default display mode. It must be defined in getDisplayModes. """
        App.Console.PrintMessage("BPSymbolViewProvider getDefaultDisplayMode \n")
        return "Standard"

    def setDisplayMode(self,mode):
        """
        Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        App.Console.PrintMessage("BPSymbolViewProvider setDisplayMode \n")
        return mode

    def onChanged(self, obj, prop):
        """ Print the name of the property that has changed """
        App.Console.PrintMessage("BPSymbolViewProvider onChanged property: " + str(prop) + "\n")

    def getIcon(self):
        return getIconPath('Symbol.svg')
