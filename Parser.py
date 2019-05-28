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

	data_pack = {'Connection_id':Controller.CONNECTION_ID,
					'Node_id':Controller.NODE_ID,
					'Nodes':node,
					'Connections':conn}
	jsonstr = json.dumps(data_pack, indent=4, sort_keys=True)
	return jsonstr
