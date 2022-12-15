# -*- coding: utf-8 -*-
###############################################################################
#
#  BluePrint.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
import FreeCADGui
import os
from PySide import QtGui, QtCore, QtSvg
#from PySide2 import QtWidgets
from decimal import *

class BluePrintGraphicsView(QtGui.QGraphicsView):

    zoom = 0

    def __init__(self):
        super().__init__()
        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        #self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setViewportUpdateMode(QtGui.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag) #ScrollHandDrag)
        self.setMouseTracking(True)

    def wheelEvent(self, event):
        #print("whell event", event)
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom += 1
        else:
            factor = 0.8
            self.zoom -= 1
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        #print("md event", event)
        super().mousePressEvent(event)

# ---------------------------------------------------------------------------------------

class BluePrintGraphicsScene(QtGui.QGraphicsScene):
    
    def __init__(self, obj):
        super().__init__()
        self.points = []
        self.curpos = None
        self.gridstep = None
        self.zoom = None
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.pen = QtGui.QPen()
        self.setGridStep(3.5429 * 5, 3.5429 * 5)
        self.obj = obj

    def drawForeground(self, g, rect):
        prev = None
        for p in self.points:
            if prev is not None and p is not None:
                g.drawLine(prev.x(), prev.y(), p.x(), p.y())
            prev = p
        if prev is not None and self.curpos is not None:
            if self.curpos.x() == prev.x() or self.curpos.y() == prev.y():
                g.drawLine(prev.x(), prev.y(), self.curpos.x(), self.curpos.y())
            else:    
                if abs(self.curpos.x()-prev.x()) < abs(self.curpos.y()-prev.y()):
                    g.drawLine(prev.x(), prev.y(), prev.x(), self.curpos.y())
                    g.drawLine(prev.x(), self.curpos.y(), self.curpos.x(), self.curpos.y())
                else:
                    g.drawLine(prev.x(), prev.y(), self.curpos.x(), prev.y())
                    g.drawLine(self.curpos.x(), prev.y(), self.curpos.x(), self.curpos.y())
        if self.obj.ShowGrid == True:
            pen = QtGui.QPen()
            pen.setStyle(QtCore.Qt.DotLine)
            pen.setWidthF(0.1)
            pen.setBrush(QtCore.Qt.gray)
            g.setPen(pen)
            gridstep = 3.5429 * 1
            for x in range(0, 450):    
                g.drawLine(QtCore.QPointF(x * gridstep, 0),QtCore.QPointF(x * gridstep, 1000))
            for y in range(0, 340):
                g.drawLine(QtCore.QPointF(0, y * gridstep),QtCore.QPointF(1500, y * gridstep))
            pen.setWidthF(0.5)
            g.setPen(pen)
            gridstep = gridstep * 10
            for x in range(0, 45):    
                g.drawLine(QtCore.QPointF(x * gridstep, 0),QtCore.QPointF(x * gridstep, 1000))
            for y in range(0, 34):
                g.drawLine(QtCore.QPointF(0, y * gridstep),QtCore.QPointF(1500, y * gridstep))

    def setGridStep(self, x, y):
        self.gridstep = QtCore.QPointF(x,y)

    def mouseReleaseEvent(self, event):
        #print("mrelease event", event)
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        #print("mdown event", event)
        curpos = event.scenePos()
        if self.gridstep is not None:
            self.curpos = QtCore.QPointF((curpos.x()+self.gridstep.x()/2)//self.gridstep.x()*self.gridstep.x(), (curpos.y()+self.gridstep.y()/2)//self.gridstep.y()*self.gridstep.y())
        else:
            self.curpos = curpos
        if event.buttons() == QtCore.Qt.LeftButton:
            if len(self.points) == 0:        
                self.points.append(self.curpos)
            else:     
                prev = self.points[-1] # last  element
                if prev is None:
                    self.points.append(self.curpos)
                else:
                    if self.curpos.x() == prev.x() or self.curpos.y() == prev.y():
                        self.points.append(self.curpos)
                    else:
                        # если длинна больше трех запоминать ход провода и не менять его.                    
                        if abs(self.curpos.x()-prev.x()) < abs(self.curpos.y()-prev.y()):
                            self.points.append(QtCore.QPointF(prev.x(), self.curpos.y()))
                            self.points.append(self.curpos)
                        else:
                            self.points.append(QtCore.QPointF(self.curpos.x(), prev.y()))
                            self.points.append(self.curpos)
        if event.buttons() == QtCore.Qt.RightButton:            
            self.points.append(None)    
        self.update()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        #print("mmove event", event)
        curpos = event.scenePos()
        if self.gridstep is not None:
            self.curpos = QtCore.QPointF((curpos.x()+self.gridstep.x()/2)//self.gridstep.x()*self.gridstep.x(), (curpos.y()+self.gridstep.y()/2)//self.gridstep.y()*self.gridstep.y())
        else:
            self.curpos = curpos        
        self.update()
        super().mouseMoveEvent(event)

#    def wheelEvent(self, event):
#        print("wevent", event)
#        super().wheelEvent(event)
 
    def clear(self):
        self.points.clear()
        self.update()
