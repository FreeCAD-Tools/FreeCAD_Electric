# -*- coding: utf-8 -*-
###############################################################################
#
#  InitGui.py
#
#  Copyright Evgeniy 2022 <>
#
###############################################################################
import FreeCADGui
import os
from PySide import QtGui, QtCore, QtSvg
#from PySide2 import QtWidgets

class BluePrintGraphicsView(QtGui.QGraphicsView):

    zoom = 0

    def __init__(self):
        super().__init__()
        #super(GraphicsView, self).__init__(parent)
        #self.setScene(self._scene)
        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        #self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setViewportUpdateMode(QtGui.QGraphicsView.ViewportUpdateMode.FullViewportUpdate)

    def wheelEvent(self, event):
        print("whell event", event)
        if event.angleDelta().y() > 0:
            factor = 1.25
            self.zoom += 1
        else:
            factor = 0.8
            self.zoom -= 1
        self.scale(factor, factor)

    def mousePressEvent(self, event):
        print("md event", event)
        super().mousePressEvent(event)

# ---------------------------------------------------------------------------------------

class BluePrintGraphicsScene(QtGui.QGraphicsScene):

    points = []
    curpos = None
    gridstep = None
    zoom = 0
    
    def __init__(self):
        super().__init__()
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.pen = QtGui.QPen()
        self.setGridStep(20, 20)

    def drawForeground(self, g, rect):
        rx = rect.x()
        ry = rect.y()
        g.drawRect(rx, ry, rect.width(), rect.height())
        g.drawRect(0, 0, 50, 50)
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

    def mouseReleaseEvent(self, event):
        print("mrelease event", event)
        super().mouseReleaseEvent(event)

    def mousePressEvent(self, event):
        print("mdown event", event)
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
        print("mmove event", event)
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
 
    def setGridStep(self, x, y):
        self.gridstep = QtCore.QPointF(x,y)

    def clear(self):
        self.points.clear()
        self.update()
