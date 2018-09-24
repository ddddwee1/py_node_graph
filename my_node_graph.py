import os 
import graph_util
from PyQt5 import QtGui, QtCore, QtWidgets
import Slots

class Node_graph(QtWidgets.QGraphicsView):
	def __init__(self, parent):
		super(Node_graph,self).__init__(parent)
		self.state = 'DEFAULT'

	def wheelEvent(self, event):

		self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)

		factor = 1.1
		if event.angleDelta().y() > 0:
			zoom = factor
		else:
			zoom = 1./factor
		self.scale(zoom, zoom)

	def mousePressEvent(self, event):
		if (event.button() == QtCore.Qt.MiddleButton):
			self.state = 'DRAGVIEW'
			self.prevPos = event.pos()
			self.setCursor(QtCore.Qt.ClosedHandCursor)
			self.setInteractive(False)
		super(Node_graph, self).mousePressEvent(event)

	def mouseMoveEvent(self, event):
		if self.state == 'DRAGVIEW':
			offset = self.prevPos - event.pos()
			self.prevPos = event.pos()
			self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
		super(Node_graph, self).mouseMoveEvent(event)

	def mouseReleaseEvent(self, event):
		if self.state == 'DRAGVIEW':
			self.setCursor(QtCore.Qt.ArrowCursor)
			self.setInteractive(True)

		self.state = 'DEFAULT'
		super(Node_graph, self).mouseReleaseEvent(event)

	def keyPressEvent(self,event):
		if event.key() == QtCore.Qt.Key_Delete:
			self._removeSelectedNodes()

	def _removeSelectedNodes(self):
		for node in self.scene().selectedItems():
			node._remove()

	def initialize(self):

		scene = NodeScene(self)
		sceneW = 3000
		sceneH = 3000
		scene.setSceneRect(0,0, sceneW, sceneH)
		self.setScene(scene)
		print('OK')

	def createNode(self, name):
		nodeItem = Node(name)

		position = self.mapToScene(self.viewport().rect().center())

		self.scene().addItem(nodeItem)
		nodeItem.setPos(position - nodeItem.nodeCenter)

		return nodeItem

	def contextMenuEvent(self, event):
		contextMenu = QtWidgets.QMenu(self)
		newAct = contextMenu.addAction('New')
		quitAct = contextMenu.addAction('Close')

		action = contextMenu.exec_(self.mapToGlobal(event.pos()))
		if action==quitAct:
			self.close()


class NodeScene(QtWidgets.QGraphicsScene):
	def __init__(self,parent):
		super(NodeScene, self).__init__(parent)

		self.gridSize = 140

	def drawBackground(self, painter, rect):
		leftLine = rect.left() - rect.left()%self.gridSize
		topLine = rect.top() - rect.top()%self.gridSize
		lines = []

		i = int(leftLine)
		while i<int(rect.right()):
			lines.append(QtCore.QLineF(i, rect.top(), i, rect.bottom()))
			i += self.gridSize

		j = int(topLine)
		while j<int(rect.bottom()):
			lines.append(QtCore.QLineF(rect.left(), j, rect.right(), j))
			j += self.gridSize

		self.pen = QtGui.QPen()
		self.pen.setColor(QtGui.QColor(80, 80, 80, 100))
		self.pen.setWidth(0)
		painter.setPen(self.pen)
		painter.drawLines(lines)

class Node(QtWidgets.QGraphicsItem):
	def __init__(self,name):
		super(Node, self).__init__()
		self.setZValue(1)
		self.setAcceptHoverEvents(True)
		self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable)
		self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)

		self.name = name 

		self.attrs = []
		self.attrs_dict = {}
		self.attr_num = 0

		self.baseWidth = 200
		self.baseHeight = 50
		self.attrHeight = 30
		self.radius = 10
		self.border = 2

		self.nodeCenter = QtCore.QPointF()
		self.nodeCenter.setX(self.baseWidth / 2.)
		self.nodeCenter.setY(self.height / 2.)

		self._pen = QtGui.QPen()
		self._pen.setStyle(QtCore.Qt.SolidLine)
		self._pen.setWidth(self.border)
		self._pen.setColor(QtGui.QColor(130, 130, 130,150))

		self._pensel = QtGui.QPen()
		self._pensel.setStyle(QtCore.Qt.SolidLine)
		self._pensel.setWidth(self.border)
		self._pensel.setColor(QtGui.QColor(170,80,80,250))

		self._brush = QtGui.QBrush()
		self._brush.setStyle(QtCore.Qt.SolidPattern)
		self._brush.setColor(QtGui.QColor(130,130,130,150))

		self._textPen = QtGui.QPen()
		self._textPen.setStyle(QtCore.Qt.SolidLine)
		self._textPen.setColor(QtGui.QColor(0,0,0,100))

		self._nodeFont = QtGui.QFont('Arial',12,QtGui.QFont.Bold)
		self._attrFont = QtGui.QFont('Arial',10,QtGui.QFont.Normal)

		self._attrBrush = QtGui.QBrush()
		self._attrBrush.setStyle(QtCore.Qt.SolidPattern)
		self._attrBrush.setColor(QtGui.QColor(100,100,100,180))

		self._attrBrush_alt = QtGui.QBrush()
		self._attrBrush_alt.setStyle(QtCore.Qt.SolidPattern)
		self._attrBrush_alt.setColor(QtGui.QColor(80,80,80,100))

	@property
	def height(self):
		if self.attr_num>0:
			return self.baseHeight + self.attrHeight*self.attr_num + self.border + 0.5 * self.radius
		else:
			return self.baseHeight
	
	def boundingRect(self):
		rect = QtCore.QRect(0, 0, self.baseWidth, self.height)
		rect = QtCore.QRectF(rect)
		return rect 

	def shape(self):
		path = QtGui.QPainterPath()
		path.addRect(self.boundingRect())
		return path 

	def paint(self, painter, option, widget):
		painter.setRenderHint(painter.Antialiasing)
		painter.setBrush(self._brush)
		if self.isSelected():
			painter.setPen(self._pensel)
		else:
			painter.setPen(self._pen)

		painter.drawRoundedRect(0,0, self.baseWidth, self.height, self.radius, self.radius)

		painter.setPen(self._textPen)
		painter.setFont(self._nodeFont)

		metrics = QtGui.QFontMetrics(painter.font())
		text_width = metrics.boundingRect(self.name).width() + 14
		text_height = metrics.boundingRect(self.name).height() + 14

		margin = (text_width - self.baseWidth) * 0.5

		textRect = QtCore.QRect(-0, -0, self.baseWidth, text_height)
		painter.drawText(textRect, QtCore.Qt.AlignCenter, self.name)

		offset = 0
		for i,attr in enumerate(self.attrs):
			rect = QtCore.QRect(self.border/2, self.baseHeight-self.radius+offset, self.baseWidth-self.border, self.attrHeight)
			if i%2==0:
				painter.setBrush(self._attrBrush)
			else:
				painter.setBrush(self._attrBrush_alt)
			painter.drawRect(rect)

			painter.setFont(self._attrFont)

			textRect = QtCore.QRect(rect.left()+self.radius, rect.top(), rect.width()-2*self.radius, rect.height())
			painter.drawText(textRect, QtCore.Qt.AlignCenter,attr)

			offset += self.attrHeight

	def mouseMoveEvent(self,event):
		# self.scene().updateScene()
		for connection in graph_util.connections:
			connection.updatePath()
		super(Node, self).mouseMoveEvent(event)

	def _remove(self):
		for k in self.attrs_dict:
			attr = self.attrs_dict[k]
			if 'plug' in attr:
				attr['plug']._remove()
			if 'socket' in attr:
				attr['socket']._remove()
		self.scene().removeItem(self)

	

	def createAttr(self, name, plug=False, socket=False):
		self.attr_num += 1
		self.attrs.append(name)
		self.attrs_dict[name] = {'name':name}

		if plug:
			plug_inst = Slots.PlugItem(self, name)
			self.attrs_dict[name]['plug'] = plug_inst
		if socket:
			socket_inst = Slots.SocketItem(self, name)
			self.attrs_dict[name]['socket'] = socket_inst

		self.update()

