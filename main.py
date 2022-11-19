import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QPoint
from IpToolbar import IpToolbar
from IpShape import *
from enum import Enum

class DrawingState(Enum):
    IDLE = 1
    DRAWING = 2
    FINISH = 3

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.img = None
        self.path_img = None
        self.cur_shape = None
        self.shape_list = []
        self.state = DrawingState.IDLE

        self.init_ui()

    def init_ui(self):

        self.toolbar = IpToolbar(self)
        self.addToolBar(self.toolbar)


        self.statusBar()

        self.setWindowTitle('Image processing')
        self.showMaximized()

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

            if self.cur_shape is not None:
                self.cur_shape.draw(painter)

            for shape in self.shape_list:
                shape.draw(painter)

    def open_image(self, path):
        self.path_img = path
        self.img = QPixmap(self.path_img)
        self.resize(self.img.width(), self.img.height())
        self.update()

def main():
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()