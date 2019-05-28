import NodeGraphBase
import graph_util
import Slots
from PyQt5 import QtGui, QtCore, QtWidgets
import Parser

class GraphNode(NodeGraphBase.Node):
	def __init__(self, name, nodeType, scene, node_id=None):
		super(GraphNode, self).__init__(name,scene, node_id)
		self.nodeType = nodeType
		attrs, attrs_dict , _ = graph_util.typeDict[nodeType]

		for attr in attrs:
			self.createAttr(attr, attrs_dict[attr]['hasPlug'], attrs_dict[attr]['hasSocket'])

class NodeGraph(NodeGraphBase.NodeGraph):
	def __init__(self,parent,graphName='MainModel'):
		super().__init__(parent)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		self.nodes = []
		self.connections = []

		self.graphName = graphName

		self.initialize()
		self.show()

	def createNode(self,name,typeName, node_id=None, position=None):
		# create new node, auto append to NodeGraph.nodes
		nodeItem = GraphNode(name,typeName, self.scene(), node_id)
		
		# self.scene().addItem(nodeItem)
		if position is None:
			position = self.mapToScene(self.viewport().rect().center())
		else:
			position = QtCore.QPointF(position[0],position[1])
		nodeItem.setPos(position - nodeItem.nodeCenter)

		# self.nodes.append(nodeItem)
		return nodeItem

	def createConnection(self, src_slot, target_slot):
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
		compAct = contextMenu.addAction('Compile')
		quitAct = contextMenu.addAction('Close')

		action = contextMenu.exec_(self.mapToGlobal(event.pos()))
		
		if action==quitAct:
			self.close()
		elif action==newAct:
			self._clear()
		elif action==saveAct:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Input dialog', 'Enter file name:')
			if ok:
				saver = self.scene().data_saver
				jsonstr = Parser.serialize(saver)
				fout = open(text+'.json','w')
				fout.write(jsonstr)
				fout.close()
		elif action==loadAct:
			text, ok = QtWidgets.QInputDialog.getText(self, 'Input dialog', 'Enter file name:')
			if ok:
				f = open(text+'.json')
				jsonstr = f.read()
				f.close()
				Parser.unserialize(self, jsonstr)
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
