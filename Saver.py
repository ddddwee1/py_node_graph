import graph_util
import json 
import Slots

def getResponse(msg):
	resp = input(msg)
	if resp in ('a','y','n',''):
		if resp=='':
			resp = 'y'
		return resp
	else:
		print('Illegal input.')
		return getResponse(msg)

def saveNodeType(fname):
	# dump node type defs 
	nodeTypeStr = json.dumps(graph_util.typeDict)
	fout = open(fname,'w')
	fout.write(nodeTypeStr)
	fout.close()

def loadNodeType(fname):
	f = open(fname)
	nodeTypeStr = f.read().strip()
	buffDict = json.loads(nodeTypeStr)
	isOverride = False
	for k in buffDict:
		if k in graph_util.typeDict:
			if not isOverride:
				resp = getResponse('Override node type: %s\ny[yes]/n[no]/a[override all]:'%k)
				if resp == 'n':
					continue
				elif resp=='a':
					isOverride = True
		graph_util.typeDict[k] = buffDict[k]

def saveGraph(fname, graph):
	nodes = []
	for node in graph.nodes:
		nodes.append([node.name,node.nodeType])

	conns = []
	for conn in graph.connections:
		src = conn.src
		target = conn.target 

		# get attr index 
		src_attr_ind = src.parent().attrs.index(src.attr)
		target_attr_ind = target.parent().attrs.index(target.attr)

		# get node index 
		src_node_ind = graph.nodes.index(src.parent())
		target_node_ind = graph.nodes.index(target.parent())

		# get type 
		if isinstance(src, Slots.SocketItem):
			src_type = 'socket'
		else:
			src_type = 'plug'

		if isinstance(target, Slots.SocketItem):
			target_type = 'socket'
		else:
			target_type = 'plug'

		# append to target
		conns.append([src_node_ind,src_attr_ind,src_type,target_node_ind,target_attr_ind,target_type])

	overAllgraph = {'nodes':nodes, 'connections':conns}

	fout = open(fname)
	fout.write(json.dumps(conns))
	fout.close()

def loadGraph(fname, nodeGraph, clearGraph=False):
	if clearGraph:
		nodeGraph._clear()
	graphStr = open(fname).read().strip()
	buffDict = json.loads(graphStr)
	nodes = buffDict['nodes']
	connections = buffDict['connections']

	for node_param in nodes:
		nodeGraph.createNode(*node_param)

	for conn_params in connections:
		nodeGraph.createConnection(*conn_params)
