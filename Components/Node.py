from typing import Optional, Sequence

from PyQt5.QtCore import QPointF, QRect, QRectF, Qt
from PyQt5.QtGui import QBrush, QColor, QFont, QFontMetrics, QPainter, QPen
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsSceneMouseEvent,
                             QStyleOptionGraphicsItem, QWidget)

from Types import NodeInfo, NodeStyle, SlotInfo
from Utils.Config import ConfigDict

from .Connection import ConnectionItem
from .Slot import SlotItem


class Node(QGraphicsItem):
    def __init__(self, cfg: ConfigDict, info: NodeInfo):
        super().__init__()
        self.cfg = cfg 
        self.name = info['name']
        # self.text = info['text']   # this is done later with set_text
        self.sockets: list[SlotItem] = []
        self.plugs: list[SlotItem] = []
        self.connections: list[ConnectionItem] = []

        self.setZValue(1)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)

        self.base_width: int = cfg.NODE.BASE_WIDTH 
        self.base_height: int = cfg.NODE.BASE_HEIGHT
        self.border: int = cfg.NODE.BORDER.WIDTH
        self.radius: int = cfg.NODE.BORDER.RADIUS

        self.create_slots(info['slots'])
        self.title_font = QFont('Times', cfg.NODE.TITLE.FONT_SIZE, QFont.Weight.Bold)
        self.text_font = QFont('Times', cfg.NODE.TEXT.FONT_SIZE, QFont.Weight.Bold)
        self.update_info(info)

        self.border_pen = QPen(QColor(*cfg.NODE.BORDER.COLOR))
        self.border_pen.setStyle(Qt.PenStyle.SolidLine)
        self.border_pen.setWidth(self.border)

        self.border_pen_sel = QPen(QColor(*cfg.NODE.BORDER.COLOR_SELECTED))
        self.border_pen_sel.setStyle(Qt.PenStyle.SolidLine)
        self.border_pen_sel.setWidth(self.border * 2)

        self.title_pen = QPen(QColor(*cfg.NODE.TITLE.TEXT_COLOR))
        self.title_pen.setStyle(Qt.PenStyle.SolidLine)

        self.text_pen = QPen(QColor(*cfg.NODE.TEXT.TEXT_COLOR))
        self.text_pen.setStyle(Qt.PenStyle.SolidLine)

        self.bg_brush = QBrush(QColor(*cfg.NODE.BACKGROUND.COLOR))
        self.bg_brush.setStyle(Qt.BrushStyle.SolidPattern)

        self.title_brush = QBrush(QColor(*cfg.NODE.TITLE.BACKGROUND_COLOR))
        self.title_brush.setStyle(Qt.BrushStyle.SolidPattern)

    def boundingRect(self) -> QRectF:
        rect = QRectF(0,0, self.base_width, self.base_height)
        return rect 

    def set_text(self, text: str):
        self.text = text
        metrics = QFontMetrics(self.text_font)
        self.base_height = self.title_h + max(len(self.sockets), len(self.plugs)) * 30 + 15 + metrics.boundingRect(self.text).height()*(self.text.count('\n')+1) + 15

    def set_title(self, name: str):
        self.name = name 
        metric = QFontMetrics(self.title_font)
        self.title_h = metric.boundingRect(self.name).height() + 14 
        self.base_width = max(metric.boundingRect(self.name).width() + 30, self.base_width)

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget] = ...) -> None:
        # draw border
        painter.setBrush(self.bg_brush)
        if self.isSelected():
            painter.setPen(self.border_pen_sel)
        else:
            painter.setPen(self.border_pen)
        painter.drawRoundedRect(0, 0, self.base_width, self.base_height, self.radius, self.radius)

        # draw title color 
        painter.setBrush(self.title_brush)
        painter.setPen(QColor(255,255,255,0))
        painter.drawRoundedRect(self.border/2,self.border/2,self.base_width-self.border, self.title_h-self.border, self.radius-1, self.radius-1)
        painter.drawRect(self.border/2, self.title_h//2, self.base_width-self.border, self.title_h//2+2)

        # write title
        painter.setFont(self.title_font)
        painter.setPen(self.title_pen)
        nameRect = QRect(0,0, self.base_width, self.title_h)
        painter.drawText(nameRect, Qt.AlignmentFlag.AlignCenter, self.name)

        if self.text:
            painter.setPen(self.text_pen)
            painter.setFont(self.text_font)
            text_start_y = self.title_h + max(len(self.sockets), len(self.plugs)) * 30 + 15
            textRect = QRect(0, text_start_y, self.base_width, self.base_height - text_start_y)
            painter.drawText(textRect, Qt.AlignHCenter, self.text)

    def update_info(self, info: NodeInfo):
        self.set_title(info['name'])
        self.set_text(info['text'])
        position = QPointF(info['pos'][0], info['pos'][1])
        self.setPos(position)

    def create_slots(self, info_list: Sequence[SlotInfo]):
        for info in info_list:
            slot_type = info['type']
            if slot_type==0:
                idx = len(self.sockets)
                slot_item = SlotItem(self, self.cfg, info, idx)
                self.sockets.append(slot_item)
            else:
                idx = len(self.plugs)
                slot_item = SlotItem(self, self.cfg, info, idx)
                self.plugs.append(slot_item)

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        # when moving the node, update all related connections 
        for conn in self.connections:
            conn.update_pos()
            conn.update_path()
            self.scene().update()
        return super().mouseMoveEvent(event)

