import cv2
from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QWidget, QSlider, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from IpShape import *

class IpToolbar(QToolBar):
    def __init__(self, parent, imagePanel, *args, **kwargs):
        super(IpToolbar, self).__init__(*args, **kwargs)

        self.parent = parent
        self.imagePanel = imagePanel

        self.init_toolbar()

    def init_toolbar(self):

        open_action = QAction(QIcon('./icons/topen.png'), 'Open', self)
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon('./icons/tsave.png'), 'Save', self)
        save_action.triggered.connect(self.save_file)

        rect_action = QAction('Rect', self)
        rect_action.setShortcut('Ctrl+R')
        rect_action.triggered.connect(lambda : self.imagePanel.set_shape(IpRectangle()))

        el_action = QAction('Ell', self)
        el_action.setShortcut('Ctrl+E')
        el_action.triggered.connect(lambda : self.imagePanel.set_shape(IpEllipse()))

        clear_action = QAction('Rest', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.imagePanel.ip.clear)


        self.addAction(open_action)
        self.addAction(save_action)
        self.addSeparator()

        self.addAction(rect_action)
        self.addAction(el_action)
        self.addSeparator()

        self.addAction(clear_action)
        self.addSeparator()

    def open_file(self, e):
        fname = QFileDialog.getOpenFileName(self, 'Open File', './')

        if fname[0]:
            self.imagePanel.open_image(fname[0])

    def save_file(self, e):
        pass