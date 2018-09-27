import my_node_graph
import graph_util
import Slots
from PyQt5 import QtGui, QtCore, QtWidgets
import Saver

class GraphNode(my_node_graph.Node):
	def __init__(self, name, nodeType, scene):
		super(GraphNode, self).__init__(name,scene)
		self.nodeType = nodeType
		attrs, attrs_dict , _ = graph_util.typeDict[nodeType]

		for attr in attrs:
			self.createAttr(attr, attrs_dict[attr]['hasPlug'], attrs_dict[attr]['hasSocket'])

class NodeGraph(my_node_graph.Node_graph):
	def __init__(self,parent,graphName='MainModel'):
		super().__init__(parent)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.nodes = []
		self.connections = []

		self.graphName = graphName

		self.initialize()
		self.show()

	def createNode(self,name,typeName,position=None):
		# create new node, auto append to NodeGraph.nodes
		nodeItem = GraphNode(name,typeName, self.scene())
		
		# self.scene().addItem(nodeItem)
		if position is None:
			position = self.mapToScene(self.viewport().rect().center())
		else:
			position = QtCore.QPointF(position[0],position[1])
		nodeItem.setPos(position - nodeItem.nodeCenter)

		# self.nodes.append(nodeItem)
		return nodeItem

	def createConnection(self, src_node_ind, src_attr_ind, target_node_ind, target_attr_ind):
		# src are auto arranged as plug and target as socket 
		src_slot = self.nodes[src_node_ind].plugs[src_attr_ind]

		target_slot = self.nodes[target_node_ind].sockets[target_attr_ind]

		# create new connection, auto append to NodeGraph.connections
		Slots.ConnectionItem(src_slot.center(),target_slot.center(),src_slot,target_slot,self.scene())

	def _clear(self):
		nodes_length = len(self.nodes)
		for i in range(len(self.nodes)-1, -1, -1):
			self.nodes[i]._remove()

	def contextMenuEvent(self, event):
		contextMenu = QtWidgets.QMenu(self)
		inputAct = contextMenu.addAction('Input Block')
		outputAct = contextMenu.addAction('Output Block')
		convAct = contextMenu.addAction('Conv Block')
		fusionAct = contextMenu.addAction('Fusion Block')
		newAct = contextMenu.addAction('New')
		saveAct = contextMenu.addAction('Save')
		loadAct = contextMenu.addAction('Load')
		quitAct = contextMenu.addAction('Close')

		action = contextMenu.exec_(self.mapToGlobal(event.pos()))
		
		if action==quitAct:
			self.close()
		elif action==newAct:
			self._clear()
		elif action==saveAct:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Save', 'Enter file name:')
			if ok:
				Saver.saveGraph(text,self)
		elif action==loadAct:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Load', 'Enter file name:')
			if ok:
				Saver.loadGraph(text,self,True)
		else:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Input dialog', 'Enter block name:')
			if action==inputAct:
				nodetype = 'startNode'
			if action==outputAct:
				nodetype = 'finalNode'
			if action==convAct:
				nodetype = 'convNode'
			if action==fusionAct:
				nodetype = 'addNode'
			if ok:
				self.createNode(text, nodetype)
