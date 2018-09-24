import my_node_graph
import graph_util
import Slots

class GraphNode(my_node_graph.Node):
	def __init__(self, name, nodeType, scene):
		super(GraphNode, self).__init__(name,scene)
		self.nodeType = nodeType
		attrs, attrs_dict = graph_util.typeDict[nodeType]

		for attr in attrs:
			self.createAttr(attr, attrs_dict[attr]['hasPlug'], attrs_dict[attr]['hasSocket'])

class NodeGraph(my_node_graph.Node_graph):
	def __init__(self,parent):
		super().__init__(parent)

		self.nodes = []
		self.connections = []

		self.initialize()
		self.show()

	def createNode(self,name,typeName,position=None):
		# create new node, auto append to NodeGraph.nodes
		nodeItem = GraphNode(name,typeName, self.scene())
		
		# self.scene().addItem(nodeItem)
		if position is None:
			position = self.mapToScene(self.viewport().rect().center())
		nodeItem.setPos(position - nodeItem.nodeCenter)

		# self.nodes.append(nodeItem)
		return nodeItem

	def createConnection(self, src_node_ind, src_attr_ind, src_type, target_node_ind, target_attr_ind, target_type):
		src_attr = self.nodes[src_node_ind].attrs[src_attr_ind]
		src_slot = self.nodes[src_node_ind].attrs_dict[src_attr][src_type]

		target_attr = self.nodes[target_node_ind].attrs[target_attr_ind]
		target_slot = self.nodes[target_node_ind].attrs_dict[target_attr][target_type]

		# create new connection, auto append to NodeGraph.connections
		Slots.ConnectionItem(src_slot.center(),target_slot.center(),src_slot,target_slot,self.scene())

	def _clear(self):
		nodes_length = len(self.nodes)
		for i in range(len(self.nodes)-1, -1, -1):
			self.nodes[i]._remove()
