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

def saveGraph(fname, nodeGraph):
	nodes = []
	for node in nodeGraph.nodes:
		nodes.append([node.name,node.nodeType,[node.pos().x(),node.pos().y()]])

	conns = []
	for conn in nodeGraph.connections:
		src = conn.src
		target = conn.target 

		# get attr index 
		src_attr_ind = src.parentItem().plugs.index(src)
		target_attr_ind = target.parentItem().sockets.index(target)

		# get node index 
		src_node_ind = nodeGraph.nodes.index(src.parentItem())
		target_node_ind = nodeGraph.nodes.index(target.parentItem())

		# src are auto arranged as plugs and target as socket

		# append to target
		conns.append([src_node_ind,src_attr_ind,target_node_ind,target_attr_ind])

	overAllgraph = {'nodes':nodes, 'connections':conns}

	fout = open(fname,'w')
	fout.write(json.dumps(overAllgraph))
	fout.close()
	return overAllgraph

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

	nodeGraph.update()
