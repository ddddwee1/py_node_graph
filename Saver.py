class Saver():
	def __init__(self):
		self.connections = []
		self.nodes = []
		self.graph = None 

	def set_graph(self, graph):
		self.graph = graph

	def remove_node(self, node):
		self.nodes.remove(node)

	def add_node(self, node):
		self.nodes.append(node)

	def remove_conn(self, conn):
		self.connections.remove(conn)

	def add_conn(self, conn):
		self.connections.append(conn)

	def get_node_idx(self, node):
		return self.nodes.index(node)

	def get_slot_idx(self, node, slot):
		if slot.is_socket:
			return node.sockets.index(slot)
		else:
			return node.plugs.index(slot)

	def serialize(self):
		nodes = []
		for node in self.nodes:
			node_info = {}
			node_info['name'] = node.name
			rect = node.boundingRect()
			x = rect.x()
			y = rect.y()
			xy = node.mapToScene(x, y)
			x = xy.x()
			y = xy.y()
			node_info['pos'] = [x,y]
			node_info['plugs'] = []
			for i in node.plugs:
				node_info['plugs'].append(i.attr)
			node_info['sockets'] = []
			for i in node.sockets:
				node_info['sockets'].append(i.attr)
			node_info['text'] = node.text if node.text else ''
			node_info['theme'] = node.theme
			nodes.append(node_info)

		conns = []
		for conn in self.connections:
			src_node_idx = self.get_node_idx(conn.src.parentItem())
			src_slot_idx = self.get_slot_idx(self.nodes[src_node_idx], conn.src)
			target_node_idx = self.get_node_idx(conn.target.parentItem())
			target_slot_idx = self.get_slot_idx(self.nodes[target_node_idx], conn.target)
			conns.append({'src': [src_node_idx, src_slot_idx], 'target': [target_node_idx, target_slot_idx]})

		res = {'nodes': nodes, 'conns': conns}
		return res 

	def deserialize_node(self, node_info):
		name = node_info['name']
		pos = node_info['pos']
		nodeItem = self.graph.createNode(name, pos)
		for i in node_info['sockets']:
			nodeItem.createSlot(i, True)
		for i in node_info['plugs']:
			nodeItem.createSlot(i, False)
		text = node_info.get('text', '')
		theme = node_info.get('theme', 0)
		nodeItem.setText(text)
		nodeItem.setTheme(theme)

	def deserialize(self, data):
		nodes = data['nodes']
		conns = data['conns']
		for node_info in nodes:
			self.deserialize_node(node_info)

		for conn in conns:
			src_idx = conn['src']
			target_idx = conn['target']
			src = self.nodes[src_idx[0]].plugs[src_idx[1]]
			target = self.nodes[target_idx[0]].sockets[target_idx[1]]
			self.graph.createConnection(src, target)

		# for c in self.connections:
		# 	c.update_path()