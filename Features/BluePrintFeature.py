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
from Features.BluePrint import BluePrintGraphicsView
from Features.BluePrint import BluePrintGraphicsScene
from Features.BPSymbolFeature import CreateBPSymbolFeature, SymbolItem
from ELLocations import getIconPath, getSymbolPath, getTemplatePath

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
        #obj.setPropertyStatus("Elements", "Hidden")
        self.obj = obj
        
        # Open file dialog filters not supported yet
        #svgFilter = "Svg files (*.svg *.SVG);;All files (*)"
        #self.obj.Template.setFilter(svgFilter)
        
        #obj.setEditorMode("Template",2)
        # https://wiki.freecadweb.org/FeaturePython_Custom_Properties
        #Blueprint property type

    def getPyObject(self):
        App.Console.PrintMessage("BluePrintFeature getPyObject \n")

    def onChanged(self, obj, prop):
        '''Do something when a property has changed'''
        App.Console.PrintMessage("BluePrintFeature Change property: " + str(prop) + "\n")
        val = obj.getPropertyByName(prop)
        if prop == "Visibility":
            if val == True:
                self.createTabIfItNotExists(obj)   # Needs to open mdi tab again
            else:
                self.frame.close()            
        if prop == "Template":
            self.createTabIfItNotExists(obj)
        #if prop == "Elements":
        #    print(val)
            # Вызывается при удалении добавлении объектов

    def createTabIfItNotExists(self,obj):
        if 'frame' in locals(): # and self.frame is not None:
            return
        self.scene = self.createTestScene()
        self.view = BluePrintGraphicsView()
        self.view.setBackgroundBrush(QtGui.Qt.gray)
        self.view.setScene(self.scene)
        self.addTab(obj)
        # Set Template
        svg_template = QtSvg.QGraphicsSvgItem(obj.Template)
        self.scene.svg_template = self.scene.addItem(svg_template)
        svg_template.setPos(0,0)
        svg_template.setZValue(-1) # Qreal from -1 ... 1
        # Fit scene to view
        #self.scene.setSceneRect(0,0,200,300)

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

#http://it.kgsu.ru/Python_Qt/oglav16.html

    def createTestScene(self):
        '''create test scene'''
        self.scene = BluePrintGraphicsScene()
        #framecolor = QtGui.QPen(QtGui.Qt.black)
        #backcolor = QtGui.QBrush(QtGui.Qt.white)
        #self.scene.line1 = self.scene.addLine(10,115,490,216)
        #self.scene.ellipse = self.scene.addEllipse(20,20,100,50)
        #pen = QtGui.QPen(QtGui.Qt.red)
        #self.scene.rect = self.scene.addRect(20,20,80,80,pen)
        #self.scene.rect.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        #self.scene.line2 = self.scene.addLine(40,40,80,80)
        #self.scene.line2.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        return self.scene

    def onDocumentRestored(self, obj):
        App.Console.PrintMessage("BluePrintFeature onDocumentRestored " + str(obj) + " \n")

    def execute(self, obj):
        """ Called on document recompute """
        App.Console.PrintMessage("BluePrintFeature execute \n")

    def getScene(self):
        #s = Gui.Selection.getSelectionEx()[0].Object.Proxy.getScene()
        return self.scene

    def shapeSetPosAndmakeMovable(self, item, x=0, y=0):
        item.setPos(x, y)
        item.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        item.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        #item.setFlag(QtGui.QGraphicsItem.ItemClipsToShape)
        item.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges)
        #item.setElementId("")

    def addShadow(self, item, radius=10, xOffset=5, yOffset=5):
        shadow = QtGui.QGraphicsDropShadowEffect()
        shadow.setBlurRadius(radius)
        shadow.setXOffset(xOffset)
        shadow.setYOffset(yOffset)
        # Добавление эффекта к объекту
        item.setGraphicsEffect(shadow)   

    def addShape(self, name, x=0, y=0):
        #svg = QtSvg.QGraphicsSvgItem(getSymbolPath(name))
        
        symbol = CreateBPSymbolFeature(self, name, x, y)
        e = self.obj.Elements
        e.append(symbol)
        self.obj.Elements = e
        
        #renderer = QtSvg.QSvgRenderer()
        #svg = SymbolItem(symbol, self.obj)
        #svg.setSharedRenderer(renderer)
        #svg.renderer().load(getSymbolPath(name+".svg"))   # The problem is that when using the QSvgRenderer to load the .svg then 
        #                                # the boundingRect of the QGraphicsSvgItem is not updated so nothing will be drawn
        #svg.setElementId("")       # Solution is to use passing an empty string to the setElementId method to recalculate bounding box

        #svg.setCursor(QtCore.Qt.SizeAllCursor)
        #svg.setToolTip("This object is signal lamp it turned on after user press the gren button. It shows than pump motor is start to working.")
        ##svg.setRotation(45) # Почему-то при повороте выводится все изображение
        ##svg.setParentItem(parentItem) # For move grouping
        
        #svgitem = self.scene.addItem(svg) 
        #self.shapeSetPosAndmakeMovable(svg, x, y)

    def addLabel(self, text, x=0, y=0, font=labelfont):
        textitem = self.scene.addText(text, font)
        self.shapeSetPosAndmakeMovable(textitem, x, y)
        textitem.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.addShadow(textitem)
        return textitem        

'''
from PySide import QtGui, QtCore, QtSvg
s.
mainWindow = FreeCADGui.getMainWindow()
mdiArea = mainWindow.findChild(QtGui.QMdiArea) # Find QMdiArea at MainWindow
subWindow = mdiArea.addSubWindow(view)
subWindow.show()
mdiArea.setActiveSubWindow(subWindow)
tab = mainWindow.findChildren(QtGui.QTabBar)[0]
tab.setTabText(tab.count()-2,"jjj")
s =  Gui.Selection.getSelectionEx()[0]
'''
#mdiArea.activateNextSubWindow()
#mdiArea.activatePreviousSubWindow()

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