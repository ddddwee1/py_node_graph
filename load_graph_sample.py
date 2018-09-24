from PyQt5 import QtWidgets
import NodeGraph
import Saver

app = QtWidgets.QApplication([])

# start: graph main body

node_graph = NodeGraph.NodeGraph(None)
Saver.loadGraph('graph0.json',node_graph,clearGraph=True)
# end: graph main body

app.exec_()
