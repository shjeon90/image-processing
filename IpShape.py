from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import QPoint, Qt, QRect

class IpShape:
    def __init__(self):
        self.init_point = None
        self.cur_point = None

    def init(self, p: QPoint):
        self.init_point = p

    def update(self, p: QPoint):
        self.cur_point = p

    def draw(self, painter: QPainter):
        pass

class IpRectangle(IpShape):
    def __init__(self):
        super(IpRectangle, self).__init__()

    def draw(self, painter: QPainter):
        if self.init_point is None or self.cur_point is None: return

        painter.setPen(QPen(Qt.blue, 1))
        r = QRect(self.init_point, self.cur_point)
        painter.drawRect(r.normalized())

class IpEllipse(IpShape):
    def __init__(self):
        super(IpEllipse, self).__init__()

    def draw(self, painter: QPainter):
        if self.init_point is None or self.cur_point is None: return

        painter.setPen(QPen(Qt.blue, 1))
        r = QRect(self.init_point, self.cur_point)
        painter.drawEllipse(r.normalized())