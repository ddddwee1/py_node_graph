from PyQt5 import QtCore, QtWidgets
import my_node_graph

app = QtWidgets.QApplication([])

# graph main body
node_graph = my_node_graph.Node_graph(None)
node_graph.initialize()
node_graph.show()

nodea = node_graph.createNode('Node1')
nodea.createAttr('attr1',plug=True,socket=True)
nodea.createAttr('attr2')

nodeb = node_graph.createNode('Node2')
nodeb.createAttr('attr3',plug=True)
# end: graph main body

app.exec_()
