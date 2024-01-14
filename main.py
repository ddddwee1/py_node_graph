import sys

from PyQt5.QtWidgets import QApplication

from Base import MainWindow
from Types import NodeInfo, SlotInfo
from Utils import Config


if __name__=='__main__':
    app = QApplication(sys.argv)
    cfg = Config.load_yaml('config_default.yaml')

    # view = NodeGraph.NodeGraph(None, cfg)
    view = MainWindow.Window(cfg)
    manager = view.manager
    slot1: SlotInfo = {'attr': 'att1', 'max_connections':1, 'type':1}
    slot2: SlotInfo = {'attr': 'att2', 'max_connections':1, 'type':0}
    info: NodeInfo = {'name': 'Title', 'pos':[5000,5000], 'text': 'texttext', 'slots':[slot1, slot2, slot2]}
    manager.create_node(info)
    info2: NodeInfo = {'name': 'Title', 'pos':[4500,5000], 'text': 'texttext', 'slots':[slot1, slot2, slot2]}
    manager.create_node(info2)
    view.show()

    app.exec_()
