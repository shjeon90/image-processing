import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Demo(QtWidgets.QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.resize(600, 600)

        self.pix = QtGui.QPixmap(600, 600)
        self.pix.fill(QtCore.Qt.white)
        self.begin_point, self.end_point = QtCore.QPoint(), QtCore.QPoint()

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)
        painter.drawPixmap(QtCore.QPoint(), self.pix)

        if not self.begin_point.isNull() and not self.end_point.isNull():
            r = QtCore.QRect(self.begin_point, self.end_point)
            painter.drawRect(r.normalized())

    def mousePressEvent(self, event):
        if event.button() & QtCore.Qt.LeftButton:
            self.begin_point = event.pos()
            self.end_point = self.begin_point
            self.update()

    def mouseMoveEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self.end_point = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() & QtCore.Qt.LeftButton:
            r = QtCore.QRect(self.begin_point, self.end_point)
            painter = QtGui.QPainter(self.pix)
            painter.drawRect(r.normalized())
            self.begin_point = self.end_point = QtCore.QPoint()
            self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())