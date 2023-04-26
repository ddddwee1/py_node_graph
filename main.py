import sys
from PyQt5.QtWidgets import QApplication
import NodeGraph

if __name__=='__main__':
    app = QApplication(sys.argv)

    view = NodeGraph.NodeGraph(None)
    view.initialize()
    view.show()

    app.exec_()
