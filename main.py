import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap
from IpToolbar import IpToolbar
from IpImagePanel import *

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()

        self.img = None
        self.path_img = None

        self.init_ui()

    def init_ui(self):
        self.imagePanel = IpImagePanel(self)

        self.toolbar = IpToolbar(self, self.imagePanel)
        self.addToolBar(self.toolbar)

        self.setCentralWidget(self.imagePanel)

        self.setWindowTitle('Image processing')
        self.showMaximized()


def main():
    app = QApplication(sys.argv)
    my_app = MyApp()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()