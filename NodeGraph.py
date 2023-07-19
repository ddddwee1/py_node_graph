import typing
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QPoint, QPointF, Qt
from PyQt5.QtGui import QBrush, QColor, QPen
import Saver 
import json 
import glob

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
        self.saver = Saver.Saver()

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
        self.setWindowTitle('NodeGraph')
        self.filename = None
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        factor = 1.1
        if event.angleDelta().y() > 0:
            zoom = factor
        else:
            zoom = 1. / factor
        
        if self.zoom_level*zoom <0.3 or self.zoom_level*zoom>1.3:
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
        scene.saver.set_graph(self)
        self.setScene(scene)
        print('Scene initialized.')

        # n1 = self.createNode('abc')
        # n1 = self.createNode('cde')

    def createNode(self, name, pos=None):
        nodeItem = Node(name, self.scene())

        if pos is None:
            position = QPointF(self.w/2, self.h/2)
            nodeItem.setPos(position)
            nodeItem.createSlot('etet', True)
            nodeItem.createSlot('etet2', True)
            nodeItem.createSlot('', False)
            nodeItem.createSlot('etet4', False)
            nodeItem.setText('GOGOGO\nfgg')
        else:
            position = QPointF(pos[0], pos[1])
            nodeItem.setPos(position)
        return nodeItem

    def createConnection(self, src, target):
        conn = ConnectionItem(self.scene(), src, target, None, None)
        # conn.update_path()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            nodes = self.scene().nodes
            for i in range(len(nodes)-1, -1, -1):
                n = nodes[i]
                if n.isSelected():
                    n._remove()

        # shift shortcuts 
        if (event.modifiers() & Qt.ControlModifier):
            if event.key() == QtCore.Qt.Key_S:
                self._on_save()
            if event.key() == QtCore.Qt.Key_L:
                self._on_load()
            if event.key() == QtCore.Qt.Key_N:
                self._on_new()

    def removeAllNodes(self):
        for i in range(len(self.scene().nodes)-1, -1, -1):
            self.scene().nodes[i]._remove()

    def _on_new(self):
        self.removeAllNodes()
        self.filename = None

    def _on_save(self):
        if self.filename is None:
            text, ok = QtWidgets.QInputDialog.getText(self, 'Input dialog', 'Enter file name:')
            if ok:
                data = self.scene().saver.serialize()
                json.dump(data, open(text+'.json', 'w'), indent=4)
                self.filename = text
        else:
            data = self.scene().saver.serialize()
            json.dump(data, open(self.filename+'.json', 'w'), indent=4)

    def contextMenuEvent(self, event):
        contextMenu = QtWidgets.QMenu(self)
        newAct = contextMenu.addAction('New')
        loadAct = contextMenu.addAction('Load')
        saveAct = contextMenu.addAction('Save')
        addAct = contextMenu.addAction('Add Node')

        action = contextMenu.exec_(self.mapToGlobal(event.pos()))
        if action==newAct:
            self._on_new()
        elif action==saveAct:
            self._on_save()
        elif action==loadAct:
            dialog = LoadFileDialog()
            ret = dialog.exec_()
            if ret:
                res = dialog.get_values()
                text = res
                data = json.load(open(text +'.json'))
                self.scene().saver.deserialize(data)
                self.filename = text
        elif action==addAct:
            dialog = EditNodeDialog()
            ret = dialog.exec_()
            if ret:
                res = dialog.get_values()
                pos = self.mapToScene(event.pos())
                res['pos'] = [pos.x(), pos.y()]
                self.scene().saver.deserialize_node(res)


class Node(QtWidgets.QGraphicsItem):
    def __init__(self, name: str, scene: QtWidgets.QGraphicsScene, text='', theme=0):
        super().__init__()
        self.name = name 
        self.text = text 
        self.theme = theme

        self.setZValue(1)
        self.setAcceptHoverEvents(True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

        self.baseWidth = 200
        self.baseHeight = 200
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

        self._nodeFont = QtGui.QFont('Times', 25, QtGui.QFont.Bold)
        # self.text_h = 20
        metrics = QtGui.QFontMetrics(self._nodeFont)
        self.text_h = metrics.boundingRect(self.name).height() + 14
        self.baseWidth = max(metrics.boundingRect(self.name).width() + 30, self.baseWidth)

        self._textFont = QtGui.QFont('Times', 14, QtGui.QFont.Bold)
        self._textPenSmall = QtGui.QPen()
        self._textPenSmall.setStyle(Qt.SolidLine)
        self._textPenSmall.setColor(QColor(25,70,159,255))

        scene.addItem(self)
        scene.nodes.append(self)
        scene.saver.add_node(self)

        self.sockets = []
        self.plugs = []
        self.setTheme(self.theme)

        metrics = QtGui.QFontMetrics(self._textFont)
        self.baseHeight = self.text_h + max(len(self.sockets), len(self.plugs)) * 30 + 15 + metrics.boundingRect(self.text).height()*(self.text.count('\n')+1) + 5

    def setText(self, text):
        self.text = text
        metrics = QtGui.QFontMetrics(self._textFont)
        self.baseHeight = self.text_h + max(len(self.sockets), len(self.plugs)) * 30 + 15 + metrics.boundingRect(self.text).height()*(self.text.count('\n')+1) + 5

    def setTheme(self, theme):
        self.theme = theme % 5
        if theme==0:
            self._titlebrush.setColor(QColor(68,114,196,255))
            self._textPenSmall.setColor(QColor(25,70,159,255))
        elif theme==1:
            self._titlebrush.setColor(QColor(102,158,64,255))
            self._textPenSmall.setColor(QColor(84,130,53,255))
        elif theme==2:
            self._titlebrush.setColor(QColor(255,197,13,255))
            self._textPenSmall.setColor(QColor(157,130,60,255))
        elif theme==3:
            self._titlebrush.setColor(QColor(238,137,68,255))
            self._textPenSmall.setColor(QColor(110,50,10,255))
        elif theme==4:
            self._titlebrush.setColor(QColor(234,112,112,255))
            self._textPenSmall.setColor(QColor(168,24,24,255))
        for i in self.sockets:
            i.setTheme(theme)
        for i in self.plugs:
            i.setTheme(theme)
        
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
        text_h = self.text_h

        # draw title color 
        painter.setBrush(self._titlebrush)
        painter.setPen(QColor(255,255,255,0))
        painter.drawRoundedRect(self.border/2,self.border/2,self.baseWidth-self.border, text_h-self.border, self.radius-1, self.radius-1)
        painter.drawRect(self.border/2, text_h//2, self.baseWidth-self.border, text_h//2+2)

        # write text
        painter.setPen(self._textPen)
        nameRect = QtCore.QRect(0,0, self.baseWidth, text_h)
        painter.drawText(nameRect, Qt.AlignCenter, self.name)

        if self.text:
            painter.setPen(self._textPenSmall)
            painter.setFont(self._textFont)
            text_start_y = text_h + max(len(self.sockets), len(self.plugs)) * 30 + 15
            textRect = QtCore.QRect(0, text_start_y, self.baseWidth, self.baseHeight - text_start_y)
            painter.drawText(textRect, Qt.AlignHCenter, self.text)

    def createSlot(self, attr, is_socket):
        slot = SlotItem(self, attr, is_socket)
        slot.setTheme(self.theme)
        if is_socket:
            self.sockets.append(slot)
        else:
            self.plugs.append(slot)
        metrics = QtGui.QFontMetrics(self._textFont)
        self.baseHeight = self.text_h + max(len(self.sockets), len(self.plugs)) * 30 + 15 + metrics.boundingRect(self.text).height()*(self.text.count('\n')+1) + 5

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        for conn in self.scene().connections:
            conn.update_path()
        super().mouseMoveEvent(event)

    def _remove(self):
        for i in self.sockets:
            i._remove()
        for i in self.plugs:
            i._remove()
        scene = self.scene()
        scene.nodes.remove(self)
        scene.saver.remove_node(self)
        scene.removeItem(self)
        scene.update()

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
        self._font = QtGui.QFont('Times', 10, 15) 

        self.is_socket = is_socket
        self.radius = 12
        self.interval = 30

        self.y_ind = len(self.parentItem().sockets) if is_socket else len(self.parentItem().plugs)

        self.new_conn = None
        self.conns = []

    def setTheme(self, theme):
        if theme==0:
            self._brush.setColor(QColor(47, 85, 151, 255))
        elif theme==1:
            self._brush.setColor(QColor(108, 166, 68, 255))
        elif theme==2:
            self._brush.setColor(QColor(234, 178, 0, 255))
        elif theme==3:
            self._brush.setColor(QColor(130, 120, 50, 255))
        elif theme==4:
            self._brush.setColor(QColor(230, 78, 30, 255))

    def center(self):
        rect = self.boundingRect()
        center = QPointF(rect.x()+rect.width()*0.5, rect.y()+rect.height()*0.5)
        center = self.mapToScene(center)
        return center

    def paint(self, painter: QtGui.QPainter, option: 'QtWidgets.QStyleOptionGraphicsItem', widget: typing.Optional[QtWidgets.QWidget] = ...) -> None:
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

    def _remove(self):
        for i in range(len(self.conns)-1, -1, -1):
            conn = self.conns[i]
            conn._remove()

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
        scene.saver.add_conn(self)
        if isinstance(src, SlotItem):
            src.conns.append(self)
        if isinstance(target, SlotItem):
            target.conns.append(self)

        self._pen = QPen(QColor(0,0,0,255))
        self._pen.setWidth(2)
        self.update_path()

    def update_path(self):
        if self.src is not None:
            self.src_pos = self.src.center()
        if self.target is not None:
            self.target_pos = self.target.center()
        # print(self.src_pos, self.target_pos)
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
        # super().mousePressEvent(event)

    def mouseMoveEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        if self.target is None:
            self.target_pos = event.pos()
        if self.src is None:
            self.src_pos = event.pos()
        self.update_path()

    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent') -> None:
        self._onMouseRelease(event)
        # self._switch_src_target()
        super().mouseReleaseEvent(event)

    def _remove(self):
        scene = self.scene()
        scene.connections.remove(self)
        if isinstance(self.src, SlotItem):
            if self in self.src.conns:
                self.src.conns.remove(self)
        if isinstance(self.target, SlotItem):
            if self in self.target.conns:
                self.target.conns.remove(self)
        scene.saver.remove_conn(self)
        scene.removeItem(self)
        scene.update()
    
    def _onMouseRelease(self, event: QtWidgets.QGraphicsSceneMouseEvent):
        slot = self.scene().itemAt(event.scenePos().toPoint(), QtGui.QTransform())
        if not isinstance(slot, SlotItem):
            self._remove()
            return 
        if self.target is None:
            if slot.accept_slot(self.src):
                self.target = slot 
                if not self in self.src.conns:
                    self.src.conns.append(self)
                if not self in self.target.conns:
                    self.target.conns.append(self)
                self.update_path()
            else:
                self._remove()
        elif self.src is None:
            if slot.accept_slot(self.target):
                self.src = slot 
                if not self in self.src.conns:
                    self.src.conns.append(self)
                if not self in self.target.conns:
                    self.target.conns.append(self)
                self.update_path()
            else:
                self._remove()
        else:
            self._remove()

    def _switch_src_target(self):
        if self.src.is_socket:
            self.src, self.target = self.target, self.src
            self.update_path()


class EditNodeDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        name_label = QtWidgets.QLabel()
        name_label.setText('Name')
        self.box_name = box_name = QtWidgets.QLineEdit()

        plugs_label = QtWidgets.QLabel()
        plugs_label.setText('Plugs')
        self.box_plugs = box_plugs = QtWidgets.QPlainTextEdit()
        box_plugs.setMaximumHeight(60)

        sockets_label = QtWidgets.QLabel()
        sockets_label.setText('Sockets')
        self.box_sockets = box_sockets = QtWidgets.QPlainTextEdit()
        box_sockets.setMaximumHeight(60)

        text_label = QtWidgets.QLabel()
        text_label.setText('Text')
        self.box_text = box_text = QtWidgets.QPlainTextEdit()
        box_text.setMaximumHeight(60)
        style_label = QtWidgets.QLabel()
        style_label.setText('Theme')
        self.box_style = box_style = QtWidgets.QLineEdit()

        layout.addWidget(name_label)
        layout.addWidget(box_name)
        layout.addWidget(plugs_label)
        layout.addWidget(box_plugs)
        layout.addWidget(sockets_label)
        layout.addWidget(box_sockets)
        layout.addWidget(text_label)
        layout.addWidget(box_text)
        layout.addWidget(style_label)
        layout.addWidget(box_style)

        btn = QtWidgets.QPushButton('OK')
        btn.pressed.connect(self.okok)
        button_layout.addWidget(btn)

        btn = QtWidgets.QPushButton('Cancel')
        btn.pressed.connect(self.on_cancel)
        button_layout.addWidget(btn)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setWindowTitle('Add Node')

    def okok(self):
        self.done(1)

    def on_cancel(self):
        self.done(0)

    def get_values(self):
        name = self.box_name.text()
        plugs = self.box_plugs.toPlainText().strip('\n')
        sockets = self.box_sockets.toPlainText().strip('\n')
        try:
            res = {'name': name}
            res['plugs'] = []
            res['sockets'] = []
            res['text'] = self.box_text.toPlainText().replace('\\n', '\n')
            try:
                res['theme'] = int(self.box_style.text()) % 5
            except:
                res['theme'] = 0

            if plugs:
                plugs = plugs.split('\n')
                for i in plugs:
                    i = i.strip()
                    res['plugs'].append(i)

            if sockets:
                sockets = sockets.split('\n')
                for i in sockets:
                    i = i.strip()
                    res['sockets'].append(i)

        except Exception as e:
            print(e)
            print('Error input text')
        return res 


class LoadFileDialog(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()

        name_label = QtWidgets.QLabel()
        name_label.setText('Files')
        self.fileslist = QtWidgets.QListWidget(self)
        layout.addWidget(name_label)
        layout.addWidget(self.fileslist)

        btn = QtWidgets.QPushButton('OK')
        btn.pressed.connect(self.okok)
        button_layout.addWidget(btn)

        btn = QtWidgets.QPushButton('Cancel')
        btn.pressed.connect(self.on_cancel)
        button_layout.addWidget(btn)
        layout.addLayout(button_layout)
        self.setLayout(layout)
        self.setWindowTitle('Load File')

        files = glob.glob('./*.json')
        for f in files:
            f = f.replace('\\', '/').split('/')[-1].replace('.json', '')
            item = QtWidgets.QListWidgetItem(f)
            self.fileslist.addItem(item)

    def okok(self):
        self.done(1)

    def on_cancel(self):
        self.done(0)

    def get_values(self):
        name = self.fileslist.currentItem().text()
        print(name)
        return name 


if __name__=='__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    import NodeGraph

    app = QApplication(sys.argv)

    view = NodeGraph.NodeGraph(None)
    view.initialize()
    view.show()

    app.exec_()


