from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtCore import QPoint
from enum import Enum
from IpShape import *
from IpImageProcess import *
from utils import *

class DrawingState(Enum):
    IDLE = 1
    DRAWING = 2
    FINISH = 3

class IpImagePanel(QWidget):
    def __init__(self, *args, **kwargs):
        super(IpImagePanel, self).__init__(*args, **kwargs)
        self.parent = args[0]

        self.state = DrawingState.IDLE
        self.cur_shape = None
        self.shape_list = []

        self.img = None
        self.ip = IpImageProcess(self)

    def set_shape(self, shape):
        self.cur_shape = shape

    def mousePressEvent(self, e):
        if self.cur_shape is not None and \
                self.img is not None and \
                self.state is DrawingState.IDLE:

            self.state = DrawingState.DRAWING
            self.cur_shape.init(e.pos())
            self.update()

    def mouseMoveEvent(self, e):
        if self.state is DrawingState.DRAWING:
            self.cur_shape.update(e.pos())
            self.update()

    def mouseReleaseEvent(self, e):
        if self.state is DrawingState.DRAWING:
            self.state = DrawingState.IDLE
            self.shape_list.append(self.cur_shape)
            self.update()

            if isinstance(self.cur_shape, IpRectangle):
                self.cur_shape = IpRectangle()
            elif isinstance(self.cur_shape, IpEllipse):
                self.cur_shape = IpEllipse()
            else:
                self.cur_shape = None

    def paintEvent(self, e):
        if self.img is not None:
            painter = QPainter(self)
            painter.drawPixmap(QPoint(), self.img)
            # painter.drawPixmap(self.rect(), self.img)

            if self.cur_shape is not None:
                self.cur_shape.draw(painter)

            for shape in self.shape_list:
                shape.draw(painter)

    def open_image(self, path):
        self.path_img = path

        self.img = QPixmap(self.path_img).toImage()
        self.img = self.img.convertToFormat(QImage.Format.Format_Grayscale8)
        self.img = QPixmap.fromImage(self.img)
        self.img_orig = self.img.copy()

        self.setFixedSize(self.img.size())

        # self.update()
        self.repaint()
        self.parent.setFixedSize(self.parent.sizeHint())