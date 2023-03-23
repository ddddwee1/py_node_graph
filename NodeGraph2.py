import typing
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen

class NodeScene(QtWidgets.QGraphicsScene):
    def __init__(self, parent):
        super().__init__(parent)
        self.pen = QtGui.QPen()
        self.pen.setColor(QtGui.QColor(180, 180, 180, 150))
        self.pen.setWidth(0)
        self.grid_size = 140
        self.setBackgroundBrush(QColor(255,255,230,255))

        self.nodes = []
        self.connections = []

    def drawBackground(self, painter: QtGui.QPainter, rect: QtCore.QRectF) -> None:
        super().drawBackground(painter, rect)
        # left_line = rect.left() - rect.left() % self.grid_size
        # top_line = rect.top() - rect.top() % self.grid_size
        limitw, limith = self.parent().w, self.parent().h
        lines = []
        i = 0
        while i < int(limitw):
            lines.append(QtCore.QLineF(i, 0, i, limith))
            i += self.grid_size

        j = 0
        while j < int(limith):
            lines.append(QtCore.QLineF(0, j, limitw, j))
            j += self.grid_size

        painter.setPen(self.pen)
        painter.drawLines(lines)

class NodeGraph(QtWidgets.QGraphicsView):
    def __init__(self, parent):
        super().__init__(parent)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.state = 'DEFAULT'
        self.prevPos = 0
        self.w = 10000
        self.h = 10000
        self.zoom_level = 1.0

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        factor = 1.1
        if event.angleDelta().y() > 0:
            zoom = factor
        else:
            zoom = 1. / factor
        
        if self.zoom_level*zoom <0.5 or self.zoom_level*zoom>1.3:
            zoom = 1 
        self.scale(zoom, zoom)
        self.zoom_level *= zoom

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == QtCore.Qt.MiddleButton:
            self.state = 'DRAGVIEW'
            self.prevPos = event.pos()
            self.setCursor(QtCore.Qt.ClosedHandCursor)
            self.setInteractive(False)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.state == 'DRAGVIEW':
            offset = self.prevPos - event.pos()
            self.prevPos = event.pos()
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
            self.update()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if self.state == 'DRAGVIEW':
            self.setCursor(QtCore.Qt.ArrowCursor)
            self.setInteractive(True)
        self.state = 'DEFAULT'
        super().mouseReleaseEvent(event)

    def initialize(self):
        scene = NodeScene(self)
        
        scene.setSceneRect(0, 0, self.w, self.h)
        self.setScene(scene)
        print('Scene initialized.')

        n1 = self.createNode('abc')
        n1 = self.createNode('cde')

    def createNode(self, name):
        nodeItem = Node(name, self.scene())
        position = QPointF(self.w/2, self.h/2)
        nodeItem.setPos(position)
        nodeItem.createSlot('etet', True)
        nodeItem.createSlot('etet2', True)
        nodeItem.createSlot('etet33233', False)
        nodeItem.createSlot('etet4', False)

        return nodeItem

class Node(QtWidgets.QGraphicsItem):
    def __init__(self, name: str, scene: QtWidgets.QGraphicsScene):
        super().__init__()
        self.name = name 

        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.baseWidth = 200
        self.baseHeight = 250
        self.border = 2
        self.radius = 10

        self.nodeCenter = QtCore.QPointF()
        self.nodeCenter.setX(self.baseWidth / 2.)
        self.nodeCenter.setY(self.height / 2.)

        self._pen = QtGui.QPen()
        self._pen.setStyle(Qt.SolidLine)
        self._pen.setWidth(self.border)
        self._pen.setColor(QColor(100, 100, 100, 255))

        self._pensel = QtGui.QPen()
        self._pensel.setStyle(Qt.SolidLine)
        self._pensel.setWidth(self.border*2)
        self._pensel.setColor(QColor(178, 80, 80, 250))

        self._brush = QtGui.QBrush()
        self._brush.setStyle(Qt.SolidPattern)
        self._brush.setColor(QColor(230, 230, 230, 255))

        self._textPen = QtGui.QPen()
        self._textPen.setStyle(Qt.SolidLine)
        self._textPen.setColor(QColor(255,255,255,255))

        self._titlebrush = QtGui.QBrush()
        self._titlebrush.setStyle(Qt.SolidPattern)
        self._titlebrush.setColor(QColor(68,114,196,255))

        self._nodeFont = QtGui.QFont('Arial', 20, QtGui.QFont.Bold)
        self.text_h = 20

        scene.addItem(self)
        scene.nodes.append(self)

        self.sockets = []
        self.plugs = []
        
    @property
    def height(self):
        return self.baseHeight

    def boundingRect(self) -> QtCore.QRectF:
        rect = QtCore.QRectF(0,0, self.baseWidth, self.height)
        return rect 

    def paint(self, painter: QtGui.QPainter, option: 'QtWidgets.QStyleOptionGraphicsItem', widget: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        painter.setBrush(self._brush)
        if self.isSelected():
            painter.setPen(self._pensel)
        else:
            painter.setPen(self._pen)
        painter.drawRoundedRect(0,0, self.baseWidth, self.height, self.radius, self.radius)

        # compute title wh 
        painter.setFont(self._nodeFont)
        # calculate the text width/height -> margin 
        metrics = QtGui.QFontMetrics(painter.font())
        # text_w = metrics.boundingRect(self.name).width() + 14
        text_h = metrics.boundingRect(self.name).height() + 14
        self.text_h = text_h
        # margin = (text_w - self.baseWidth) / 2 

        # draw title color 
        painter.setBrush(self._titlebrush)
        painter.setPen(QColor(255,255,255,0))
        painter.drawRoundedRect(self.border/2,self.border/2,self.baseWidth-self.border, text_h-self.border, self.radius, self.radius)
        painter.drawRect(self.border/2, text_h//2, self.baseWidth-self.border, text_h//2+2)

        # write text
        painter.setPen(self._textPen)
        textRect = QtCore.QRect(0,0, self.baseWidth, text_h)
        painter.drawText(textRect, Qt.AlignCenter, self.name)

    def createSlot(self, attr, is_socket):
        slot = SlotItem(self, attr, is_socket)
        if is_socket:
            self.sockets.append(slot)
        else:
            self.plugs.append(slot)

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        for conn in self.scene().connections:
            conn.update_path()
        super().mouseMoveEvent(event)

class SlotItem(QtWidgets.QGraphicsItem):
    def __init__(self, parent: typing.Optional['QtWidgets.QGraphicsItem'], attr: str, is_socket: bool) -> None:
        super().__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.attr = attr 
        self.setZValue(4)

        self._brush = QBrush()
        self._brush.setStyle(Qt.SolidPattern)
        self._brush.setColor(QColor(25,60,90,255))

        self._pen = QPen()
        self._pen.setStyle(Qt.SolidLine)
        self._pen.setColor(QColor(25,60,90,255))
        self._pen.setWidth(4)
        self._nothing = QPen(QColor(255,255,255,0))
        self.current_pen = self._nothing

        self._textPen = QPen()
        self._textPen.setStyle(Qt.SolidLine)
        self._textPen.setColor(QColor(0,0,0,255))
        self._font = QtGui.QFont('Arial', 10, 15) 

        self.is_socket = is_socket
        self.radius = 10
        self.interval = 30

        self.y_ind = len(self.parentItem().sockets) if is_socket else len(self.parentItem().plugs)

        self.new_conn = None

    def center(self):
        rect = self.boundingRect()
        center = QPointF(rect.x()+rect.width()*0.5, rect.y()+rect.height()*0.5)
        return self.mapToScene(center)

    def paint(self, painter: QtGui.QPainter, option: 'QtWidgets.QStyleOptionGraphicsItem', widget: typing.Optional[QtWidgets.QWidget] = ...) -> None:
        # super().paint(painter, option, widget)
        painter.setBrush(self._brush)
        painter.setPen(self.current_pen)
        painter.drawEllipse(self.boundingRect())

        painter.setFont(self._font)
        # calculate the text width/height -> margin 
        metrics = QtGui.QFontMetrics(painter.font())
        text_w = metrics.boundingRect(self.attr).width() + 14
        text_h = metrics.boundingRect(self.attr).height() + 14
        if self.is_socket:
            y = self.parentItem().text_h + self.radius + self.interval * self.y_ind + 5 - text_h/2 + self.radius/2
            x = 14 + 10 
        else:
            y = self.parentItem().text_h + self.radius + self.interval * self.y_ind + 5 - text_h/2 + self.radius/2
            x = self.parentItem().baseWidth - 21 - text_w
        painter.setPen(self._textPen)
        textRect = QtCore.QRect(x,y, text_w, text_h)
        painter.drawText(textRect, Qt.AlignCenter, self.attr)

    def hoverEnterEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent') -> None:
        super().hoverEnterEvent(event)
        self.current_pen = self._pen

    def hoverLeaveEvent(self, event: 'QtWidgets.QGraphicsSceneHoverEvent') -> None:
        super().hoverLeaveEvent(event)
        self.current_pen = self._nothing

    def boundingRect(self) -> QtCore.QRectF:
        width = height = self.radius
        if self.is_socket:
            y = self.parentItem().text_h + self.radius + self.interval * self.y_ind + 5
            x = 14
        else:
            y = self.parentItem().text_h + self.radius + self.interval * self.y_ind + 5
            x = self.parentItem().baseWidth - 21
        rect = QtCore.QRectF(x,y,width, height)
        return rect 
    
    def accept_slot(self, slot):
        if (self.is_socket ^ slot.is_socket) and (self.parentItem() != slot.parentItem()):
            return True
        return False
    
    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        if event.button()==QtCore.Qt.LeftButton:
            # self.parentItem().setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, enabled=False)
            if self.is_socket:
                self.new_conn = ConnectionItem(self.scene(), src=None, target=self, src_pos=self.mapToScene(event.pos()), target_pos=self.center())
            else:
                self.new_conn = ConnectionItem(self.scene(), src=self, target=None, src_pos=self.center(), target_pos=self.mapToScene(event.pos()))
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        if self.new_conn.target is None:
            self.new_conn.target_pos = self.mapToScene(event.pos())
        else:
            self.new_conn.src_pos = self.mapToScene(event.pos())
        self.new_conn.update_path()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        self.new_conn._onMouseRelease(event)
        super().mouseReleaseEvent(event)

class ConnectionItem(QtWidgets.QGraphicsPathItem):
    def __init__(self, scene, src:SlotItem, target:SlotItem, src_pos, target_pos) -> None:
        super().__init__()
        self.src = src 
        self.target = target
        self.src_pos = src_pos
        self.target_pos = target_pos

        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.setZValue(0)
        
        scene.addItem(self)
        scene.connections.append(self)

        self._pen = QPen(QColor(0,0,0,255))
        self._pen.setWidth(2)
        self.update_path()

    def update_path(self):
        if self.src is not None:
            self.src_pos = self.src.center()
        if self.target is not None:
            self.target_pos = self.target.center()
        self.setPen(self._pen)
        path = QtGui.QPainterPath()
        path.moveTo(self.src_pos)

        dx = (self.target_pos.x() - self.src_pos.x()) * 0.5
        dy = self.target_pos.y() - self.src_pos.y()
        if dx>0 or (self.target is None) or (self.src is None):
            ctrl1 = QtCore.QPointF(self.src_pos.x()+dx, self.src_pos.y()+dy*0)
            ctrl2 = QtCore.QPointF(self.src_pos.x()+dx, self.src_pos.y()+dy*1)
        else:
            ctrl1 = QtCore.QPointF(self.src_pos.x()-dx*1.5, self.src_pos.y()+dy*0.5)
            ctrl2 = QtCore.QPointF(self.src_pos.x()+dx*3.5, self.src_pos.y()+dy*0.5)
        path.cubicTo(ctrl1, ctrl2, self.target_pos)
        self.setPath(path)

    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        d2target = (event.pos() - self.target_pos).manhattanLength()
        d2source = (event.pos() - self.src_pos).manhattanLength()
        if d2target<d2source:
            self.target_pos = event.pos()
            self.target = None
        else:
            self.src_pos = event.pos()
            self.src = None 
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        if self.target is None:
            self.target_pos = event.pos()
        if self.src is None:
            self.src_pos = event.pos()
        self.update_path()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        self._onMouseRelease(event)
        super().mouseReleaseEvent(event)

    def _remove(self):
        scene = self.scene()
        scene.connections.remove(self)
        scene.removeItem(self)
        scene.update()
    
    def _onMouseRelease(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        slot = self.scene().itemAt(event.scenePos().toPoint(), QtGui.QTransform())
        print(type(slot))
        if not isinstance(slot, SlotItem):
            self._remove()
            return 
        if self.target is None:
            if slot.accept_slot(self.src):
                self.target = slot 
                self.update_path()
            else:
                self._remove()
        elif self.src is None:
            if slot.accept_slot(self.target):
                self.src = slot 
                self.update_path()
            else:
                self._remove()
        else:
            self._remove()

if __name__=='__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    import NodeGraph

    app = QApplication(sys.argv)

    view = NodeGraph.NodeGraph(None)
    view.initialize()
    view.show()

    app.exec_()
