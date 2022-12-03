# -*- coding: utf-8 -*-
###############################################################################
#
#  ELCommands.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
import FreeCAD
import FreeCAD as App
import FreeCADGui
import os
from PySide import QtGui, QtCore, QtSvg
from Features.BluePrint import BluePrintGraphicsView
from Features.BluePrint import BluePrintGraphicsScene
from ELLocations import getSymbolPath

def CreateBluePrintFeature():
    obj_name = 'BluePrint'
    obj = App.ActiveDocument.addObject('App::FeaturePython', obj_name)
    BluePrintFeature(obj)
    BluePrintViewProvider(obj.ViewObject)
    App.ActiveDocument.recompute()

class BluePrintFeature():

    scene = None
    view = None

    def __init__(self, obj):
        """ Default constructor """
        self.Type = 'BluePrintFeature'
        obj.Proxy = self
        obj.addProperty('App::PropertyString', 'Description', 'Base', 'Box description').Description = ""
        obj.addProperty('App::PropertyLength', 'Width', 'Page', 'Page width').Width = '100 mm'
        obj.addProperty('App::PropertyLength', 'Height', 'Page', 'Page height').Height = '100 mm'

    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, obj):
        """ Called on document recompute """
        FreeCAD.Console.PrintMessage("Execute \n")
        self.scene = self.createTestScene()
        view = BluePrintGraphicsView()
        view.setBackgroundBrush(QtGui.Qt.gray)
        view.setScene(self.scene)
        view.setMouseTracking(True)
        self.addMDIView(view,obj.Name)
        self.view = view

    def createTestScene(self):
        '''create test scene'''
        scene = BluePrintGraphicsScene()
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
        
        but = QtSvg.QGraphicsSvgItem(getSymbolPath('Button.svg'))
        scene.svg1 = scene.addItem(but) 
        but.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        but.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        
        rc = QtSvg.QGraphicsSvgItem(getSymbolPath('RelayCoil.svg'))
        scene.svg1 = scene.addItem(rc) 
        rc.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        rc.setFlag(QtGui.QGraphicsItem.ItemIsSelectable) 
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

class BluePrintViewProvider:

    def __init__(self, obj):
        """ Set this object to the proxy object of the actual view provider """
        print("BluePrint Viewprovider init")
        obj.Proxy = self

    def getDetailPath(self, subname, path, append):
        FreeCAD.Console.PrintMessage("getDetailPath: " + str(subname) + " " + str(path) + " " + str(append) + "\n")
   
    def getElementPicked(self, pp):
        FreeCAD.Console.PrintMessage("getElementPicked: " + pp.getPath() + "\n")

    def attach(self, obj):
        """ Setup the scene sub-graph of the view provider, this method is mandatory """
        print("BluePrint Viewprovider attach")
        return

    def updateData(self, fp, prop):
        """ If a property of the handled feature has changed we have the chance to handle this here """
        print("BluePrint Viewprovider updateData")
        return

    def getDisplayModes(self, obj):
        """ Return a list of display modes. """
        print("BluePrint Viewprovider getDisplayModes")
        #modes=[]
        #modes.append("Normal")
        return [] #modes

    def getDefaultDisplayMode(self):
        """ Return the name of the default display mode. It must be defined in getDisplayModes. """
        print("BluePrint Viewprovider getDefaultDisplayMode")
        return "" #"Normal"

    def setDisplayMode(self,mode):
        """
        Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        print("BluePrint Viewprovider setDisplayMode")
        return mode

    def onChanged(self, vp, prop):
        """ Print the name of the property that has changed """
        App.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def getIcon(self):
        """ Return the icon in XMP format which will appear in the tree view. This method is optional and if not defined a default icon is shown. """

        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "    c None",
            ".   c #141010",
            "+   c #615BD2",
            "@   c #C39D55",
            "#   c #000000",
            "$   c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        """ Called during document saving. """
        print("BluePrint Viewprovider __getstate__")
        return None

    def __setstate__(self,state):
        """ Called during document restore. """
        print("BluePrint Viewprovider __setstate__")
        return None