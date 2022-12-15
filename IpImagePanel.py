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
    PERSPECTIVE = 4

class IpImagePanel(QWidget):
    def __init__(self, *args, **kwargs):
        super(IpImagePanel, self).__init__(*args, **kwargs)
        self.parent = args[0]

        self.state = DrawingState.IDLE
        self.cur_shape = None
        self.shape_list = []
        self.perspective_pts = []

        self.img = None
        self.ip = IpImageProcess(self)

    def clear(self):
        self.state = DrawingState.IDLE
        self.cur_shape = None
        self.shape_list.clear()
        self.perspective_pts.clear()

    def set_shape(self, shape):
        self.cur_shape = shape

    def set_perspective(self):
        self.state = DrawingState.PERSPECTIVE

    def perspective_transform(self):
        perspective_pts = np.array(self.perspective_pts).astype(np.float32)
        w1 = np.abs(perspective_pts[1, 0] - perspective_pts[0, 0])
        w2 = np.abs(perspective_pts[2, 0] - perspective_pts[3, 0])
        h1 = np.abs(perspective_pts[2, 1] - perspective_pts[0, 1])
        h2 = np.abs(perspective_pts[3, 1] - perspective_pts[1, 1])

        width = int(np.max([w1, w2]))
        height = int(np.max([h1, h2]))

        pts2 = np.array([
            [0., 0.], [width-1, 0.],
            [0., height-1], [width-1, height-1]
        ]).astype(np.float32)

        img_gray, alpha = self.ip.get_gray_alpha()

        T = cv2.getPerspectiveTransform(perspective_pts, pts2)
        img_per = cv2.warpPerspective(img_gray, T, (width, height))
        cv2.imshow('perspective', img_per)



    def mousePressEvent(self, e):
        if self.cur_shape is not None and \
                self.img is not None and \
                self.state is DrawingState.IDLE:

            self.state = DrawingState.DRAWING
            self.cur_shape.init(e.pos())
            self.update()
        elif self.state is DrawingState.PERSPECTIVE:
            if len(self.perspective_pts) < 4:
                self.perspective_pts.append(
                    np.array([e.x(), e.y()])
                )

            if len(self.perspective_pts) == 4:
                self.ip.perspective_transformation(self.perspective_pts)
                self.perspective_pts.clear()
                self.state = DrawingState.IDLE

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

            for pt in self.perspective_pts:
                painter.setPen(QPen(Qt.blue, 1))
                r = QRect(QPoint(pt[0]-2, pt[1]-2), QPoint(pt[0]+2, pt[1]+2))
                painter.drawEllipse(r.normalized())

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