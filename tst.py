import NodeGraphBase
from PyQt5 import QtWidgets
import NodeGraph

app = QtWidgets.QApplication([])

# node_graph = NodeGraphBase.NodeGraph(None)
# node_graph.initialize()
# node_graph.show()
node_graph = NodeGraph.NodeGraph(None)

app.exec_()
