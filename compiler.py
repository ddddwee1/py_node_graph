import json 
import Saver 
import NodeGraph
import graph_util

class Node():
	def __init__(self,name,nodeType):
		self.parent = []
		self.childs = []
		self.name = name 
		self.nodeType = nodeType

		self.attrs, self.attrs_dict,self.func = graph_util.typeDict[nodeType]
		self.plugs = []
		self.sockets = []
		for att in self.attrs:
			buff = self.attrs_dict[att]
			if buff['hasPlug']:
				self.plugs.append(att)
			if buff['hasSocket']:
				self.sockets.append(att)

	def addParent(self,node):
		if not node in self.parent:
			self.parent.append(node)

	def addChild(self,node):
		if not node in self.childs:
			self.childs.append(node)

def build_nodes(nodes):
	res = []
	for n in nodes:
		node = Node(*n[:2])
		res.append(node)
	return res 

def construct_tree(graph_dict):
	nodes = build_nodes(graph_dict['nodes'])
	conn_list = graph_dict['connections']
	connections = []
	for conn in conn_list:
		buff = [[conn[3],nodes[conn[0]],conn[1]] , [conn[1], nodes[conn[2]] , conn[3]]]
		connections.append(buff)

	for conn in connections:
		# I dont know why i write like this
		conn[0][1].addParent(conn[1])
		conn[1][1].addChild(conn[0])

	root_nodes = [n for n in nodes if len(n.parent)==0]
	return root_nodes

def compile(nodeGraph,fname=None):
	graph_dict = Saver.saveGraph('temp_graph.json',nodeGraph)

	node_list = construct_tree(graph_dict)

	lines = []

	index = 0
	max_index = len(node_list)
	while index<max_index:
		node = node_list[index]

		func_name = node.func

		input_args = []
		for child in node.childs:
			arg_ind = child[0]
			arg_name = node.sockets[arg_ind]
			child_node = child[1]
			child_arg_ind = child[2]
			child_name = child_node.name
			if node.nodeType!='finalNode':
				arg_str = arg_name+'='
			else:
				arg_str = ''
			if len(child_node.plugs)==1:
				arg_str += child_name + '_output'
			else:
				arg_str += child_name + '_output[%d]'%child_arg_ind
			input_args.append(arg_str)
			if not child_node in node_list:
				node_list.append(child_node)
		max_index = len(node_list)

		code_line = node.name + '_output = %s(%s)'%(func_name,','.join(input_args))
		# exception for outnode
		if node.nodeType=='finalNode':
			code_line = '%s %s'%(func_name,','.join(input_args))
		lines.append(code_line)

		index+=1
	lines = lines[::-1]
	for line in lines:
		print(line)

	if not fname is None:
		fout = open(fname,'w')
		for line in lines:
			fout.write(line + '\n')
