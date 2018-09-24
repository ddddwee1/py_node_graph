from PyQt5 import QtWidgets
import NodeGraph
import Saver

app = QtWidgets.QApplication([])

# start: graph main body

node_graph = NodeGraph.NodeGraph(None)
node_graph.createNode('convNode1','convNode')
node_graph.createNode('convNode2','convNode')
node_graph.createNode('convNode3','convNode')
node_graph.createNode('addNode1','addNode')
# end: graph main body

app.exec_()
Saver.saveGraph('graph0.json', node_graph)
