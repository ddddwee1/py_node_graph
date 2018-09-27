from PyQt5 import QtWidgets
import NodeGraph
import Saver
import compiler 

app = QtWidgets.QApplication([])

# start: graph main body
node_graph = NodeGraph.NodeGraph(None)
# node_graph.createNode('Input','startNode')
# node_graph.createNode('Conv','convNode')
# node_graph.createNode('Classifier','convNode')
# node_graph.createNode('Softmax','convNode')
# node_graph.createNode('evalLayer','finalNode')
# end: graph main body

app.exec_()
# Saver.saveGraph('graph0.json', node_graph)
compiler.compile(node_graph, fname='temp_code.py')