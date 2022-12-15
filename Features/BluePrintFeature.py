# -*- coding: utf-8 -*-
###############################################################################
#
#  BluePrintFeature.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
import FreeCAD
import FreeCAD as App
import FreeCADGui
import os
import Version
from PySide import QtGui, QtCore, QtSvg
from Features.BluePrint import BluePrintGraphicsView, BluePrintGraphicsScene
from ELLocations import getIconPath, getSymbolPath, getTemplatePath
import Features.BPSymbolFeature as Symbol

def CreateBluePrintFeature():
    obj = App.ActiveDocument.addObject('App::FeaturePython', 'BluePrint')
    BluePrintFeature(obj)
    BluePrintViewProvider(obj.ViewObject)
    return obj

class MDIViewBluePrint(QtGui.QMdiSubWindow):

    def __init__(self, obj):
        super().__init__()
        self.obj = obj
        self.setMouseTracking(True)
        self.setWindowTitle(self.obj.Name)

    def closeEvent(self, event):
        #print("Tab is closed")
        setattr(self.obj, "Visibility", False)
        FreeCADGui.Selection.removeSelection(self.obj)      # mandatory for get setSelection event in Observer if user select page again 
        super().closeEvent(event)

class BluePrintFeature():

    labelfont = QtGui.QFont("Arial", 16, 2, False)

    def __init__(self, obj):
        """ Default constructor """
        App.Console.PrintMessage("BluePrintFeature init object \n")
        self.Type = 'BluePrintFeature'
        obj.addProperty('App::PropertyString', 'Description', 'Base', 'Feature description').Description = ""
        obj.addProperty('App::PropertyFileIncluded', 'Template', 'Base', 'A slot for SVG Template file')
        if Version.ofFreeCAD() >= 20.3:
            obj.Template = {"filter" : "Svg files (*.svg *.SVG);;All files (*.*)"}
        obj.Proxy = self
        obj.addProperty('App::PropertyLinkList', 'Elements', 'Base', 'Elements list of page').Elements = []
        obj.addProperty('App::PropertyBool', 'ShowGrid', 'Base', 'Show grid True/False').ShowGrid = False
        #obj.setPropertyStatus("Elements", "Hidden")
        self.obj = obj

    def getPyObject(self):
        App.Console.PrintMessage("BluePrintFeature getPyObject \n")

    def onBeforeChange(self, obj, prop):
        val = obj.getPropertyByName(prop)
        App.Console.PrintMessage("BluePrintFeature onBeforeChange property: " + str(prop) + "=" + str(val) + "\n")
        #if prop == "Elements":
        #    for x in obj.Elements:
        #        x.Page = None
        
    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        val = obj.getPropertyByName(prop)
        App.Console.PrintMessage("BluePrintFeature Change property: " + str(prop) + "=" + str(val) + "\n")
        if prop == "Visibility":
            if val == True:
                self.createTabIfItNotExists(obj)   # Needs to open mdi tab again
            else:
                self.frame.close()            
        if prop == "Template":
            self.createTabIfItNotExists(obj)
        #if prop == "Elements":
        #    for x in obj.Elements:
        #        x.Page = obj

    def createTabIfItNotExists(self,obj):
        if 'frame' in locals(): # and self.frame is not None:
            return
        self.scene = BluePrintGraphicsScene(self.obj)
        self.view = BluePrintGraphicsView()
        self.view.setBackgroundBrush(QtGui.Qt.gray)
        self.view.setScene(self.scene)
        self.addTab(obj)
        # Set Template
        svg_template = QtSvg.QGraphicsSvgItem(obj.Template)
        self.scene.svg_template = self.scene.addItem(svg_template)
        svg_template.setPos(0,0)
        svg_template.setZValue(-1) # Qreal from -1 ... 1
        # Fit scene to view  #self.scene.setSceneRect(0,0,200,300)
        # Restoring all the elements again
        for x in obj.Elements:
            x.Proxy.createSVG()

    def addTab(self, obj):
        # Create MDIView
        self.frame = MDIViewBluePrint(obj)
        self.frame.setWidget(self.view)
        self.frame.setAttribute(QtCore.Qt.WA_DeleteOnClose)  # Destroy on close  
        mainWindow = FreeCADGui.getMainWindow()
        mdiArea = mainWindow.findChild(QtGui.QMdiArea)  # Find QMdiArea at MainWindow
        subWindow = mdiArea.addSubWindow(self.frame)    # Add QGraphicsView to this area and get QMdiSubWindow
        subWindow.show()                                # Show getted QMdiSubWindow
        mdiArea.setActiveSubWindow(subWindow)           # Activate subwindow
        tab = mainWindow.findChildren(QtGui.QTabBar)[0] # Find QTabBar
        tab.setTabText(tab.count()-1,obj.Name)          # Set text to last tab of QTabBar

    def onDocumentRestored(self, obj):
        App.Console.PrintMessage("BluePrintFeature onDocumentRestored " + str(obj) + " \n")

    def execute(self, obj):
        """ Called on document recompute """
        App.Console.PrintMessage("BluePrintFeature execute \n")

    def getScene(self):
        return self.scene

    def shapeSetPosAndmakeMovable(self, item, x=0, y=0):
        item.setPos(x, y)
        item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        item.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        #item.setElementId("")

    def addShadow(self, item, radius=10, xOffset=5, yOffset=5):
        shadow = QtGui.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(radius)
        shadow.setXOffset(xOffset)
        shadow.setYOffset(yOffset)
        item.setGraphicsEffect(shadow)   

    def addLabel(self, text, x=0, y=0, font=labelfont):
        textitem = self.scene.addText(text, font)
        self.shapeSetPosAndmakeMovable(textitem, x, y)
        textitem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.addShadow(textitem)
        return textitem

    def addItem(self, item):
        self.obj.Elements += [item]
        return

    def clearSelection(self):
        self.scene.clearSelection()

class BluePrintViewProvider:

    def __init__(self, obj):
        """ Set this object to the proxy object of the actual view provider """
        #App.Console.PrintMessage("BluePrint Viewprovider init")
        obj.addProperty('App::PropertyLength', 'Width', 'Page', 'Page width').Width = '100 mm'
        obj.addProperty('App::PropertyLength', 'Height', 'Page', 'Page height').Height = '100 mm'
        obj.setPropertyStatus("DisplayMode", "Hidden")
        self.elements = []
        obj.Proxy = self

    def updateData(self, obj, prop):
        self.elements = obj.Elements
        return

    def claimChildren(self):
        return self.elements

    def getDetailPath(self, subname, path, append):
        FreeCAD.Console.PrintMessage("BluePrintViewProvider getDetailPath: " + str(subname) + " " + str(path) + " " + str(append) + "\n")
   
    def getElementPicked(self, pp):
        FreeCAD.Console.PrintMessage("BluePrintViewProvider getElementPicked: " + str(pp) + "\n")

    def attach(self, obj):
        from pivy import coin    # Without that icon is be gray
        
        """ Setup the scene sub-graph of the view provider, this method is mandatory """
        App.Console.PrintMessage("BluePrintViewProvider attach \n")
        self.standard = coin.SoGroup()
        obj.addDisplayMode(self.standard,"Standard");
        return

    def getDisplayModes(self, obj):
        """ Return a list of display modes. """
        App.Console.PrintMessage("BluePrintViewProvider getDisplayModes \n")
        return ["Standard"]

    def getDefaultDisplayMode(self):
        """ Return the name of the default display mode. It must be defined in getDisplayModes. """
        App.Console.PrintMessage("BluePrintViewProvider getDefaultDisplayMode \n")
        return "Standard"

    def setDisplayMode(self,mode):
        """
        Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        App.Console.PrintMessage("BluePrintViewProvider setDisplayMode \n")
        return mode

    def onChanged(self, vp, prop):
        """ Print the name of the property that has changed """
        App.Console.PrintMessage("BluePrintViewProvider onChanged property: " + str(prop) + "\n")

    def getIcon(self):
        return getIconPath('BluePrint.svg')

    def __getstate__(self):
        """ Called during document saving. """
        App.Console.PrintMessage("BluePrintViewProvider __getstate__ \n")
        return None

    def __setstate__(self,state):
        """ Called during document restore. """
        App.Console.PrintMessage("BluePrintViewProvider __setstate__ \n")
        return None