import os 
import graph_util
from PyQt5 import QtGui, QtCore, QtWidgets

NON_CONNECTABLE_COLOR = [120,120,120,120]
CONNECTABLE_COLOR = [150,150,0,150]

class SlotItem(QtWidgets.QGraphicsItem):
	def __init__(self,parent,attr,max_conn=999):
		super(SlotItem, self).__init__(parent)
		self.setAcceptHoverEvents(True)

		self.attr = attr 
		self.setZValue(2)

		self.brush = QtGui.QBrush()
		self.brush.setStyle(QtCore.Qt.SolidPattern)
		self.brush.setColor(QtGui.QColor(*CONNECTABLE_COLOR))

		self.pen = QtGui.QPen()
		self.pen.setStyle(QtCore.Qt.SolidLine)
		self.pen.setColor(QtGui.QColor(*CONNECTABLE_COLOR))
		self.pen.setWidth(2)

		self.connected_slots = []
		self.connections = []
		self.max_conn = max_conn

		self.nodeRadius = 10

	def accepts(self, slot_item):
		if not ((isinstance(self, PlugItem) and isinstance(slot_item, SocketItem)) or (isinstance(self, SocketItem) and isinstance(slot_item, PlugItem))):
			return False

		if self.parentItem() == slot_item.parentItem():
			return False

		if len(self.connected_slots) >= self.max_conn:
			return False

		for conn in graph_util.connections:
			tgt = conn.target
			src = conn.src 
			if (tgt==self and src==slot_item) or (src==self and src==slot_item):
				return False

		return True

	def shape(self):
		path = QtGui.QPainterPath()
		path.addRect(self.boundingRect())
		return path 

	def paint(self, painter, option, widget):
		painter.setBrush(self.brush)
		painter.setPen(self.pen)

		nodeInst = self.scene().views()[0]
		painter.drawEllipse(self.boundingRect())

	def center(self):
		rect = self.boundingRect()
		center = QtCore.QPointF(rect.x() + rect.width()*0.5, rect.y() + rect.height()*0.5)
		return self.mapToScene(center)

	def mousePressEvent(self,event):
		if event.button()==QtCore.Qt.LeftButton:
			self.new_conn = ConnectionItem(self.center(), self.mapToScene(event.pos()), self, None)
			self.scene().addItem(self.new_conn)

	def mouseMoveEvent(self,event):
		self.new_conn.target_point = self.mapToScene(event.pos())
		self.new_conn.updatePath()

	def mouseReleaseEvent(self,event):
		self.new_conn.releaseEvent(event)
		# print(len(graph_util.connections))

	def _remove(self):
		for conn in graph_util.connections:
			if conn.src == self or conn.target == self:
				conn._remove()
		self.scene().removeItem(self)

class SocketItem(SlotItem):
	def boundingRect(self):
		width = height = self.parentItem().attrHeight * 0.5
		x = - width*0.5
		y = self.parentItem().baseHeight - self.nodeRadius + self.parentItem().attrHeight*0.25 + self.parentItem().attrs.index(self.attr)*self.parentItem().attrHeight
		rect = QtCore.QRectF(QtCore.QRect(x,y,width,height))
		return rect

class PlugItem(SlotItem):
	def boundingRect(self):
		width = height = self.parentItem().attrHeight * 0.5
		x = self.parentItem().baseWidth - width*0.5
		y = self.parentItem().baseHeight - self.nodeRadius + self.parentItem().attrHeight*0.25 + self.parentItem().attrs.index(self.attr)*self.parentItem().attrHeight
		rect = QtCore.QRectF(QtCore.QRect(x,y,width,height))
		return rect

class ConnectionItem(QtWidgets.QGraphicsPathItem):
	def __init__(self, src_point, target_point, src, target):
		super(ConnectionItem,self).__init__()
		self.setZValue(1)

		self.src_point = src_point
		self.src = src 
		self.target_point = target_point
		self.target = target

		self.setAcceptHoverEvents(True)
		self.setZValue(-1)
		self._pen = QtGui.QPen(QtGui.QColor())
		self._pen.setColor(QtGui.QColor(*CONNECTABLE_COLOR))
		self._pen.setWidth(2)
		if not self in graph_util.connections:
			graph_util.connections.append(self)

	def mousePressEvent(self, event):

		d2Target = (event.pos() - self.target_point).manhattanLength()
		d2Source = (event.pos() - self.src_point).manhattanLength()

		if d2Target<d2Source:
			self.target_point = event.pos()
			self.target = None

		else:
			self.src_point = event.pos()
			self.src = None

		self.updatePath()

	def mouseMoveEvent(self, event):
		self.movingEvent(event)
		super(ConnectionItem, self).mouseMoveEvent(event)

	def movingEvent(self, event):
		if self.target is None:
			self.target_point = event.pos()
		elif self.src is None:
			self.src_point = event.pos()
		self.updatePath()

	def mouseReleaseEvent(self,event):
		self.releaseEvent(event)

	def releaseEvent(self,event):
		slot = self.scene().itemAt(event.scenePos().toPoint(), QtGui.QTransform())

		if not isinstance(slot, SlotItem):
			self._remove()
			self.updatePath()
			super(ConnectionItem, self).mouseReleaseEvent(event)
			return 

		if self.target is None:
			if slot.accepts(self.src):
				self.target = slot
				self.target_point = slot.center()
				self.updatePath()
			else:
				self._remove()
		else:
			if slot.accepts(self.target):
				self.src = slot 
				self.src_point = slot.center()
				self.updatePath()
			else:
				self._remove()

	def _remove(self):
		scene = self.scene()
		scene.removeItem(self)
		# while self in graph_util.connections:
		graph_util.connections.remove(self)
		scene.update()

	def updatePath(self):
		self.updateSlotPos()
		self.setPen(self._pen)
		path = QtGui.QPainterPath()
		path.moveTo(self.src_point)
		dx = (self.target_point.x() - self.src_point.x()) * 0.5
		dy = self.target_point.y() - self.src_point.y()
		ctrl1 = QtCore.QPointF(self.src_point.x()+dx, self.src_point.y()+dy*0)
		ctrl2 = QtCore.QPointF(self.src_point.x()+dx, self.src_point.y()+dy*1)
		path.cubicTo(ctrl1, ctrl2, self.target_point)

		self.setPath(path)

	def updateSlotPos(self):
		if self.src is not None:
			self.src_point = self.src.center()
		if self.target is not None:
			self.target_point = self.target.center()
