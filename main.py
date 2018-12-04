from PyQt5 import QtWidgets
import NodeGraph
import Saver
import compiler 

app = QtWidgets.QApplication([])

# start: graph main body
node_graph = NodeGraph.NodeGraph(None)

app.exec_()
