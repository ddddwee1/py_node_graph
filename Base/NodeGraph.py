from typing import Literal, Optional

from PyQt5.QtCore import QLineF, QPoint, QRectF, Qt
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPen, QWheelEvent
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView

from Utils.Config import ConfigDict


class NodeScene(QGraphicsScene):
    def __init__(self, parent: 'NodeGraph', cfg: ConfigDict):
        super().__init__(parent)

        self.pen_bg_line = QPen(QColor(*cfg.BACKGROUND.LINE_COLOR))
        self.pen_bg_line.setWidth(0)
        self.setBackgroundBrush(QColor(*cfg.BACKGROUND.COLOR))

        self.graph = parent
        self.grid_size: int = cfg.BACKGROUND.GRID_SIZE
        
    def drawBackground(self, painter: QPainter, rect: QRectF) -> None:
        super().drawBackground(painter, rect)

        limitw, limith = self.graph.w, self.graph.h

        # draw lines
        lines: list[QLineF] = [] 
        i = 0
        while i<int(limitw):
            lines.append(QLineF(i, 0, i, limith))
            i += self.grid_size
        
        j = 0
        while j<int(limith):
            lines.append(QLineF(0, j, limitw, j))
            j += self.grid_size
        
        painter.setPen(self.pen_bg_line)
        painter.drawLines(*lines)


class NodeGraph(QGraphicsView):
    state: Literal['dragging', 'rest']
    prev_position: Optional[QPoint]

    def __init__(self, parent, cfg: ConfigDict):
        super().__init__(parent)
        self.cfg = cfg 

        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.w = 10000
        self.h = 10000
        self.zoom_level = 1.0 
        self.zoom_factor: float = cfg.BACKGROUND.ZOOM_FACTOR
        self.zoom_upper: float = cfg.BACKGROUND.ZOOM_UPPER 
        self.zoom_lower: float = cfg.BACKGROUND.ZOOM_LOWER
        self.state = 'rest'
        self.prev_position = None
        self.setWindowTitle('NodeGraph')
        
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        scene = NodeScene(self, cfg)
        scene.setSceneRect(0, 0, self.w, self.h)
        self.setScene(scene)
        self.selected_node = None

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        if event.angleDelta().y() > 0: 
            zoom = self.zoom_factor
        else:
            zoom = 1 / self.zoom_factor
        
        if self.zoom_level * zoom < self.zoom_lower or self.zoom_level * zoom > self.zoom_upper:
            zoom = 1 
        self.scale(zoom, zoom)
        self.zoom_level *= zoom 
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        # if clicked, set to dragging state 
        if event.button() == Qt.LeftButton:
            itm = self.itemAt(event.pos())
            if itm is None:
                if self.selected_node is not None:
                    self.selected_node.setSelected(False)
                    self.selected_node = None
                self.state = 'dragging'
                self.prev_position = event.pos()
                self.setCursor(Qt.ClosedHandCursor)
                self.setInteractive(False)
            else:
                self.selected_node = itm
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # drag the view ~
        if self.state=='dragging':
            if self.prev_position is not None:
                offset: QPoint = self.prev_position - event.pos()
                self.prev_position = event.pos()

                self.verticalScrollBar().setValue(self.verticalScrollBar().value() + offset.y())
                self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + offset.x())
                # self.update()
        return super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self.state=='dragging':
            self.setCursor(Qt.ArrowCursor)
            self.setInteractive(True)
            self.state = 'rest'
        return super().mouseReleaseEvent(event)
    
