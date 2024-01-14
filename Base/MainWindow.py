from PyQt5.QtWidgets import QMainWindow, QMenu

from Utils.Config import ConfigDict
from Utils.NodeManager import NodeManager

from . import NodeGraph


class Window(QMainWindow):
    def __init__(self, cfg: ConfigDict, parent=None):
        super().__init__(parent)

        graph_view = NodeGraph.NodeGraph(self, cfg)
        self.setCentralWidget(graph_view)

        self._createMenuBar()
        self.setWindowTitle('NodeGraph')

        self.manager = NodeManager(cfg, graph_view)
        self.setGeometry(cfg.POSITION.XOFFSET, cfg.POSITION.YOFFSET, cfg.POSITION.W, cfg.POSITION.H)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # Creating menus using a QMenu object
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        # Creating menus using a title
        editMenu = menuBar.addMenu("&Edit")
        helpMenu = menuBar.addMenu("&Help")

    def create_node(self, info):
        self.manager.create_node(info)
