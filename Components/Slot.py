from typing import TYPE_CHECKING, Optional

from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsSceneHoverEvent,
                             QGraphicsSceneMouseEvent,
                             QStyleOptionGraphicsItem, QWidget)

from Types import SlotInfo
from Utils.Config import ConfigDict

from .Connection import ConnectionItem

if TYPE_CHECKING:
    from .Node import Node


class SlotItem(QGraphicsItem):
    def __init__(self, parent, cfg: ConfigDict, info: SlotInfo, y_idx: int) -> None:
        super().__init__(parent)
        self.cfg = cfg 

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.y_idx = y_idx
        self.attr = info['attr']
        self.slot_type = info['type']  # 0 for socket 1 for plug
        self.max_connections = info['max_connections']
        self.connected: int = 0
        self.radius = cfg.SLOT.CIRCLE.RADIUS 
        self.interval = cfg.SLOT.CIRCLE.INTERVAL
        self.setZValue(4)

        self.circle_brush = QBrush(QColor(*cfg.SLOT.CIRCLE.COLOR))
        self.circle_brush.setStyle(Qt.BrushStyle.SolidPattern)

        self.border_pen = QPen(QColor(*cfg.SLOT.CIRCLE.COLOR))
        self.border_pen.setStyle(Qt.PenStyle.SolidLine)
        self.border_pen.setWidth(4)

        self.transparant_pen = QPen(QColor(255,255,255,0))
        self.transparant_pen.setStyle(Qt.PenStyle.SolidLine)

        self.current_pen = self.transparant_pen

        self.text_pen = QPen(QColor(0,0,0,255))
        self.text_pen.setStyle(Qt.PenStyle.SolidLine)
        self.text_font = QFont('Times', cfg.SLOT.TEXT.SIZE, cfg.SLOT.TEXT.WEIGHT)

        self.new_connection = None 

    def boundingRect(self) -> QRectF:
        parent: Node = self.parentItem()
        y = parent.title_h + self.radius + self.interval * self.y_idx + self.cfg.SLOT.MARGIN_TITLE
        if self.slot_type==0:
            x = self.cfg.SLOT.PAD_LEFT
        else:
            x = parent.base_width - self.cfg.SLOT.PAD_RIGHT
        rect = QRectF(x, y, self.radius, self.radius)
        return rect

    def center_in_scene(self) -> QPointF:
        rect = self.boundingRect()
        center = QPointF(rect.x()+rect.width()*0.5, rect.y()+rect.height()*0.5)
        center = self.mapToScene(center)
        return center
    
    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        # draw circle 
        painter.setBrush(self.circle_brush)
        painter.setPen(self.current_pen)
        painter.drawEllipse(self.boundingRect())

        # write text
        painter.setFont(self.text_font)
        painter.setPen(self.text_pen)
        metrics = QFontMetrics(self.text_font)
        text_w = metrics.boundingRect(self.attr).width() 
        text_h = metrics.boundingRect(self.attr).height() 

        parent: Node = self.parentItem()
        y = parent.title_h + self.radius/2 + self.interval * (self.y_idx + 0.5) - text_h / 2 + self.cfg.SLOT.TEXT.PAD_TOP
        if self.slot_type==0:
            x = self.cfg.SLOT.PAD_LEFT + self.radius + self.cfg.SLOT.TEXT.PAD_SIDE
        else:
            x = parent.base_width - self.cfg.SLOT.PAD_RIGHT - self.cfg.SLOT.TEXT.PAD_SIDE - text_w
        textRect = QRectF(x, y, text_w, text_h)
        painter.drawText(textRect, Qt.AlignmentFlag.AlignHCenter, self.attr)

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.current_pen = self.border_pen
        return super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        self.current_pen = self.transparant_pen
        return super().hoverLeaveEvent(event)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.button()==Qt.MouseButton.LeftButton:
            if self.slot_type==0:
                self.new_connection = ConnectionItem(self.cfg, None, self, self.scene().parent().parent().manager)
            if self.slot_type==1:
                self.new_connection = ConnectionItem(self.cfg, self, None, self.scene().parent().parent().manager)
        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.new_connection is not None:
            self.new_connection.auto_set_position(event.scenePos().toPoint())
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        if self.new_connection is not None:
            self.new_connection.try_finish(event)
            self.new_connection = None
        return super().mouseReleaseEvent(event)

