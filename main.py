from PyQt5 import QtCore, QtWidgets
import NodeGraph

app = QtWidgets.QApplication([])

# start: graph main body

node_graph = NodeGraph.NodeGraph(None)
node_graph.createNode('Node1',typeName='sampleNode')
node_graph.createNode('Node2',typeName='sampleNode')
# end: graph main body

app.exec_()
