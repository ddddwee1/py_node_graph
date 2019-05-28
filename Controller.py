
NODE_ID = 10000
CONNECTION_ID = 30000

class DataSaver():
	def __init__(self):
		self.nodes = []
		self.connections = []
	def add_node(self, obj):
		self.nodes.append(obj)
		#print(self.nodes)
	def remove_node(self, obj):
		self.nodes.remove(obj)
		#print(self.nodes)
	def add_connection(self, obj):
		self.connections.append(obj)
		#print(self.connections)
	def remove_connection(self, obj):
		self.connections.remove(obj)
		#print(self.connections)
