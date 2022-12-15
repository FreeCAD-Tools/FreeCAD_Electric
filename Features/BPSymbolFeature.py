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

def Create(page, name, x=0, y=0):
    obj = App.ActiveDocument.addObject('App::FeaturePython', name)    
    BPSymbolFeature(obj, page, name, x, y)
    BPSymbolViewProvider(obj.ViewObject)
    page.Proxy.addItem(obj)
    return obj

class BPSymbolFeature():

    def __init__(self, obj, page, name, x, y):
        App.Console.PrintMessage("BPSymbolFeature init object \n")
        self.Type = 'BPSymbolFeature'
        obj.addProperty('App::PropertyString', 'Description', 'Base', 'Feature description').Description = ""
        obj.addProperty('App::PropertyLink', 'Page', 'Base', 'Page were element is presented').Page = page
        obj.addProperty('App::PropertyString', 'ElementType', 'Data', 'Element type: Lamp, Rely etc...').ElementType = name
        obj.addProperty('App::PropertyFloat', 'X', 'Position', 'X position on sheet').X = x
        obj.addProperty('App::PropertyFloat', 'Y', 'Position', 'Y position on sheet').Y = y
        obj.Proxy = self
        self.obj = obj
        self.createSVG()

    def onDocumentRestored(self, obj):
        App.Console.PrintMessage("BPSymbolFeature onDocumentRestored " + str(obj) + " \n")
        self.createSVG()

    def execute(self, obj):
        App.Console.PrintMessage("BPSymbolFeature execute \n")  

    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        self.obj = obj
        val = obj.getPropertyByName(prop)
        App.Console.PrintMessage("BPSymbolFeature Change property: " + str(prop) + "=" + str(val) + "\n")
        #if item with elemntid in scene not exist add item to scene
        if not hasattr(self,"item"):
            return
        if prop == "X":
            self.item.setPos(val, obj.Y)
        if prop == "Y":
            self.item.setPos(obj.X, val)
        if prop == "Page":
            if val == None:
                self.onDelete()
            else:
                self.onRestore()            

    def createSVG(self):
        renderer = QtSvg.QSvgRenderer()
        svg = SymbolItem(self.obj)
        svg.setSharedRenderer(renderer)
        svg.renderer().load(getSymbolPath(self.obj.ElementType+".svg"))   # The problem is that when using the QSvgRenderer to load the .svg then 
                                        # the boundingRect of the QGraphicsSvgItem is not updated so nothing will be drawn
        svg.setElementId("")       # Solution is to use passing an empty string to the setElementId method to recalculate bounding box

        svg.setCursor(QtCore.Qt.SizeAllCursor)
        svg.setToolTip("This object is signal lamp it turned on after user press the gren button. It shows than pump motor is start to working.") 
        svg.setPos(self.obj.X, self.obj.Y)
        svg.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        svg.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        svg.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        svg.setElementId("")
        self.item = svg
        #self.bpf.scene.addItem(svg)
        self.obj.Page.Proxy.getScene().addItem(self.item)
        print(svg.boundingRect())
        #svg.setTransformOriginPoint(svg.boundingRect().bottom()/2,svg.boundingRect().right()/2)  

    def onDelete(self):
        #self.obj.Page.Proxy.getScene().removeItem(self.item)
        #print('hide')
        self.item.hide() # We not delete object we hide it...

    def onRestore(self):
        #self.obj.Page.Proxy.getScene().removeItem(self.item)
        #print('show')
        self.item.show() # Restore deleted object...

    def setSelected(self, state):
        self.item.setSelected(state)

class BPSymbolViewProvider:

    def __init__(self, obj):
        """ Set this object to the proxy object of the actual view provider """
        obj.Proxy = self
        self.obj = obj

    #def onDelete(self, feature, subelements):
        #App.Console.PrintMessage("BPSymbolViewProvider onDelete " + str(feature) + " subelements: " + str(subelements) + "\n")
        #self.obj.Object.Proxy.onDelete()
        #self.obj.Object.Page = None
        #return True

    def onChanged(self, obj, prop):
        """ Print the name of the property that has changed """
        val = obj.getPropertyByName(prop)
        App.Console.PrintMessage("BPSymbolViewProvider onChanged property: " + str(prop) + "=" + str(val) + "\n")

    def updateData(self, obj, prop):
        """ If a property of the handled feature has changed we have the chance to handle this here """
        val = obj.getPropertyByName(prop)
        App.Console.PrintMessage("BPSymbolViewProvider updateData property: " + str(prop) + "=" + str(val) + "\n")

    def getIcon(self):
        return getIconPath('Symbol.svg')

    def attach(self, obj):
        from pivy import coin    # Without that icon is be gray        
        """ Setup the scene sub-graph of the view provider, this method is mandatory """
        App.Console.PrintMessage("BPSymbolViewProvider attach \n")
        self.drawingDisplayMode = coin.SoGroup()
        obj.addDisplayMode(self.drawingDisplayMode,"Drawing");
        return

    def getDisplayModes(self, obj):
        """ Return a list of display modes. """
        App.Console.PrintMessage("BPSymbolViewProvider getDisplayModes \n")
        return ["Drawing"]

    def getDefaultDisplayMode(self):
        """ Return the name of the default display mode. It must be defined in getDisplayModes. """
        App.Console.PrintMessage("BPSymbolViewProvider getDefaultDisplayMode \n")
        return "Drawing"

class SymbolItem(QtSvg.QGraphicsSvgItem):
    
    def __init__(self, obj): #, page):
        super().__init__()
        self.obj = obj
        #self.page = page

    def itemChange(self, change, value):
        #print(change)
        if change == self.ItemPositionChange:
            gridstep = 3.5429 * 5
            #print(value.x(), value.x() //  gridstep *  gridstep)
            value = QtCore.QPointF(value.x() //  gridstep *  gridstep, value.y() //  gridstep *  gridstep)
            #self.obj.X = value.x()
            #self.obj.Y = value.y()
            #self.obj.recompute()
            return value # Return value with snap to grid
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
        x = self.x()
        y = self.y()
        self.obj.X = x
        self.obj.Y = y
#        self.page.recompute()
        App.ActiveDocument.recompute()
