import json 
import Controller 

def serialize(saver):
	nodes = saver.nodes
	connections = saver.connections

	# TO-DO: Save node intrinsic parameters 

	node = {}
	for n in nodes:
		node_id = n.node_id
		node_type = n.nodeType
		node_name = n.name 
		node[node_id] = [node_type, node_name]

	conn = []
	for c in connections:
		src_id = c.src.parentItem().node_id
		src_attr = c.src.attr
		target_id = c.target.parentItem().node_id
		target_attr = c.target.attr 
		conn.append([src_id, src_attr, target_id, target_attr])

	data_pack = {'Connection_id':Controller.CONNECTION_ID, # connection id seems useless
					'Node_id':Controller.NODE_ID,
					'Nodes':node,
					'Connections':conn}
	jsonstr = json.dumps(data_pack, indent=4, sort_keys=True)
	return jsonstr

def unserialize(graph, jsonstr):
	graph._clear()

	data = json.loads(jsonstr)

	Connection_id = data['Connection_id']
	Controller.CONNECTION_ID = Connection_id
	Node_id = data['Node_id']
	Controller.NODE_ID = Node_id

	nodes = data['Nodes']
	node_dict = {}
	for n_id in nodes:
		n_type, n_name = nodes[n_id]
		node = graph.createNode(n_name, n_type, n_id)
		node_dict[int(n_id)] = node 

	conn = data['Connections']
	for (src_id, src_attr, target_id, target_attr) in conn:
		src_slot = node_dict[src_id].attrs_dict[src_attr]['plug']
		target_slot = node_dict[target_id].attrs_dict[target_attr]['socket']
		graph.createConnection(src_slot, target_slot)
