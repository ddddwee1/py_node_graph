from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import QPointF, Qt
from PyQt5.QtGui import QColor, QPainterPath, QPen, QTransform
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsPathItem,
                             QGraphicsSceneMouseEvent)

from Utils.Config import ConfigDict

if TYPE_CHECKING:
    from Utils.NodeManager import NodeManager

    from .Slot import SlotItem


class ConnectionItem(QGraphicsPathItem):
    def __init__(self, cfg: ConfigDict, start_slot: Optional['SlotItem'], end_slot: Optional['SlotItem'], manager: 'NodeManager'):
        super().__init__()

        self.manager = manager
        self.cfg = cfg 
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setZValue(0)

        self.line_pen = QPen(QColor(0,0,0,255))
        self.line_pen.setWidth(cfg.CONNECTION.WIDTH)

        self.start_slot = start_slot
        self.end_slot = end_slot
        self.start_pos: QPointF = start_slot.center_in_scene() if start_slot is not None else end_slot.center_in_scene() 
        self.end_pos: QPointF = end_slot.center_in_scene() if end_slot is not None else start_slot.center_in_scene() 

        manager.graph.scene().addItem(self)

    def update_pos(self):
        self.start_pos = self.start_slot.center_in_scene()
        self.end_pos = self.end_slot.center_in_scene()

    def update_path(self):
        self.setPen(self.line_pen)
        path = QPainterPath()
        path.moveTo(self.start_pos)

        dx = (self.end_pos.x() - self.start_pos.x()) * 0.5
        dy = self.end_pos.y() - self.start_pos.y() 
        if dx>0 or (self.start_slot is None) or (self.end_slot is None):
            ctrl1 = QPointF(self.start_pos.x()+dx, self.start_pos.y()+dy*0)
            ctrl2 = QPointF(self.start_pos.x()+dx, self.start_pos.y()+dy*1)
        else:
            ctrl1 = QPointF(self.start_pos.x()-dx*1.5, self.start_pos.y()+dy*0.5)
            ctrl2 = QPointF(self.start_pos.x()+dx*3.5, self.start_pos.y()+dy*0.5)
        path.cubicTo(ctrl1, ctrl2, self.end_pos)
        self.setPath(path)

    def auto_set_position(self, pos: QPointF):
        if self.end_slot is None:
            self.end_pos = pos
        elif self.start_slot is None:
            self.start_pos = pos 
        self.update_path()

    def auto_set_slot(self, slot: 'SlotItem'):
        if self.start_slot is None:
            if slot.connected>=slot.max_connections:
                return False
            elif self.end_slot.connected>=self.end_slot.max_connections:
                return False
            else:
                self.start_slot = slot 
                self.start_pos = slot.center_in_scene()
                return True 
        elif self.end_slot is None:
            if slot.connected>=slot.max_connections:
                return False 
            elif self.start_slot.connected>=self.start_slot.max_connections:
                return False
            else:
                self.end_slot = slot 
                self.end_pos = slot.center_in_scene()
                return True
        else:
            raise NotImplementedError

    def try_finish(self, event: QGraphicsSceneMouseEvent):
        from .Slot import SlotItem
        slot = self.scene().itemAt(event.scenePos().toPoint(), QTransform())
        if not isinstance(slot, SlotItem):
            self._remove_item()
        else:
            ret = self.auto_set_slot(slot)
            if ret:
                self.update_path()
                self.manager.update_connection(self)
                self.start_slot.connected += 1 
                self.end_slot.connected += 1 
            else:
                self._remove_item()

    def _remove_item(self):
        print('Removing connection')
        self.manager.remove_connection(self)
        scene = self.scene()
        scene.removeItem(self)
        scene.update()

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button()==Qt.MouseButton.LeftButton:
            self.start_slot.connected -= 1 
            self.end_slot.connected -= 1
            dist_start = (event.pos() - self.start_pos).manhattanLength()
            dist_end = (event.pos() - self.end_pos).manhattanLength()
            if dist_end<dist_start:
                self.end_pos = event.pos()
                self.end_slot = None
            else:
                self.start_pos = event.pos()
                self.start_slot = None
            self.update_path()
        #return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.start_slot is None:
            self.start_pos = event.pos()
        elif self.end_slot is None:
            self.end_pos = event.pos()
        self.update_path()
        # return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        self.try_finish(event)
        return super().mouseReleaseEvent(event)
