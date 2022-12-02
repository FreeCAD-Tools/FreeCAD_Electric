import FreeCADGui
import os
from PySide import QtGui, QtCore
#from PySide2 import QtWidgets

ui_name = "BluePrint.ui"
path_to_ui = os.path.dirname(__file__) + "/" + ui_name

mw = FreeCADGui.getMainWindow()

'''
class GraphicsItem(QtGui.QGraphicsObject):

    points = []
    curpos = None
    
    def __init__(self, w, h):
        super().__init__()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.width = w
        self.height = h
        self.brush = QtGui.QBrush()
        self.brush.setStyle(QtCore.Qt.SolidPattern)
        self.pen = QtGui.QPen()

    def setRect(self, x, y, w, h):
        self.setPos(x, y)
        self.width = w
        self.height = h

    def paint(self, g, option, widget):
        g.setBrush(self.brush)
        g.setPen(self.pen)
        g.drawRect(0, 0, self.width, self.height)
        prev = None
        for p in self.points:
            if prev is not None:
                g.drawLine(prev.x(), prev.y(), p.x(), p.y())
            prev = p
        if prev is not None and self.curpos is not None:
            g.drawLine(prev.x(), prev.y(), self.curpos.x(), self.curpos.y())

    def boundingRect(self):
        return QtCore.QRectF(0, 0, self.width, self.height)

    def mouseReleaseEvent(self, event):
        print("mouse release event", event)

    def mousePressEvent(self, event):
        print("mouse down event", event)
        self.points.append(event.pos())
        self.update()

    def mouseMoveEvent(self, event):
        print("mouse move event", event)
        self.curpos = event.pos()
        self.update()
        self.setPos(len(self.points), 0)
'''

# ---------------------------------------------------------------------------------------

class GraphicsView(QtGui.QGraphicsView):

    zoom = 0

    def __init__(self, parent):
        super(GraphicsView, self).__init__(parent)
        #self.setScene(self._scene)
        #self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        #self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        #self.setFrameShape(QtWidgets.QFrame.NoFrame)

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

    def wheelEvent(self, event):
        print("whell event", event)
        self.scale(scale.x()+1,scale.y()+1)

# ---------------------------------------------------------------------------------------

class GraphicsScene(QtGui.QGraphicsScene):

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
                        if abs(self.curpos.x()-prev.x()) < abs(self.curpos.y()-prev.y()):
                            self.points.append(QtCore.QPointF(prev.x(), self.curpos.y()))
                            self.points.append(self.curpos)
                        else:
                            self.points.append(QtCore.QPointF(self.curpos.x(), prev.y()))
                            self.points.append(self.curpos)
        if event.buttons() == QtCore.Qt.RightButton:            
            self.points.append(None)    
        self.update()

    def mouseMoveEvent(self, event):
        print("mmove event", event)
        curpos = event.scenePos()
        if self.gridstep is not None:
            self.curpos = QtCore.QPointF((curpos.x()+self.gridstep.x()/2)//self.gridstep.x()*self.gridstep.x(), (curpos.y()+self.gridstep.y()/2)//self.gridstep.y()*self.gridstep.y())
        else:
            self.curpos = curpos        
        self.update()

    def wheelEvent(self, event):
        print("whell event", event)

    def setGridStep(self, x, y):
        self.gridstep = QtCore.QPointF(x,y)

    def clear(self):
        self.points.clear()
        self.update()
 
# ---------------------------------------------------------------------------------------

class drawArea(QtCore.QObject):
    ''' form for simulation '''

    def __init__(self):
        super(drawArea, self).__init__()

    def initBluePrint(self):
        ''' initialise the ui, loading the graphics widgets'''

        def addToScene(brushcolor, pencolor, item):
            item.brush.setColor(brushcolor)
            item.pen.setColor(pencolor)
            self.scene.addItem(item)

        ##self.drawItem = GraphicsItem(1000, 1000)
        ##addToScene(QtGui.QColor(150, 150, 0, 16), QtGui.QColor(0, 0, 0, 255), self.drawItem)

    def eventFilter(self, object, event):
        ''' handle resize events for the freecad ui '''
        if event.type() == QtCore.QEvent.Type.Resize:
            self.setPosition()

        return False

    def setPosition(self):
        ''' position the form on the screen '''
        cen = mw.centralWidget()
        cengeom = cen.geometry()

        x = cengeom.width() * 0.1
        y = cengeom.height() - self.form.height() - 50
        newWidth = cengeom.width() * 0.8
        newHeight = self.form.height()
        self.form.setGeometry(x, y, newWidth, newHeight)

        ##self.drawItem.setRect(self.drawItem.pos().x(), self.drawItem.pos().y(), self.form.geometry().width()*0.4, self.form.geometry().height()*0.4)

    def show(self):
        #Build GUI
        self.form = FreeCADGui.PySideUic.loadUi(path_to_ui)
        self.form.setParent(mw.centralWidget())
        self.form.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.FramelessWindowHint | QtCore.Qt.CustomizeWindowHint)
        self.form.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        mw.installEventFilter(self)

        self.scene = GraphicsScene() # QtGui.QGraphicsScene()
        self.sceneContainer = self.form.progressBar
        self.sceneContainer.setScene(self.scene)
        self.scene.brush.setColor(QtGui.QColor(255, 0, 0, 16))
        self.scene.pen.setColor(QtGui.QColor(0, 0, 0, 255))

        # initialise form
        self.initBluePrint()
        self.setPosition()
        self.form.show()
        
    def clear(self):
        self.scene.clear()

    def quit(self, data=None):
        ''' handle the form being closed'''
        self.form.close()
        self.deleteLater()
