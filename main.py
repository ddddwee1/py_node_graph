from PyQt5 import QtCore, QtWidgets
import my_node_graph

app = QtWidgets.QApplication([])

# graph main body
node_graph = my_node_graph.Node_graph(None)
node_graph.initialize()
node_graph.show()

nodea = node_graph.createNode('Input')
nodea.createAttr('DataOut',plug=True,socket=True)


nodeb = node_graph.createNode('Conv1')
nodeb.createAttr('DataIn',socket=True)
nodeb.createAttr('DataOut',plug=True)

nodec = node_graph.createNode('Add1')
nodec.createAttr('DataIn1',socket=True)
nodec.createAttr('DataIn2',socket=True)
nodec.createAttr('DataOut',plug=True)

noded = node_graph.createNode('Conv2')
noded.createAttr('DataIn',socket=True)
noded.createAttr('DataOut',plug=True)
# end: graph main body

app.exec_()
