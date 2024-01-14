from typing import TYPE_CHECKING

from Components.Node import Node
from Types import NodeInfo
from Utils.Config import ConfigDict

if TYPE_CHECKING:
    from ..Base.NodeGraph import NodeGraph
    from ..Components.Connection import ConnectionItem


class NodeManager():
    def __init__(self, cfg:ConfigDict, graph: 'NodeGraph'):
        self.cfg = cfg 
        self.graph = graph 
        self.nodes: list[Node] = []
        self.connections: list[ConnectionItem] = []

    def create_node(self, info: NodeInfo):
        node_item = Node(self.cfg, info)
        self.graph.scene().addItem(node_item)
        self.nodes.append(node_item)

    def update_connection(self, conn: 'ConnectionItem'):
        self.remove_connection(conn)
        node1: Node = conn.start_slot.parentItem()
        node2: Node = conn.end_slot.parentItem()
        node1.connections.append(conn)
        node2.connections.append(conn)
        if conn not in self.connections:
            self.connections.append(conn)

    def remove_connection(self, conn: 'ConnectionItem'):
        for node in self.nodes:
            try:
                node.connections.remove(conn)
            except:
                ...
