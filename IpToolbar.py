from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QWidget, QSlider, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from IpShape import *

class ThresholdWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(ThresholdWindow, self).__init__(*args, **kwargs)

        self.parent = args[0]

        self.init()

    def init(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 255)
        slider.setSingleStep(1)
        slider.setValue(0)

        slider.valueChanged.connect(self.on_value_changed)

        self.setWindowTitle('Threshold:')

    def on_value_changed(self, e):
        self.parent.ip.set_threshold(e)

class IpToolbar(QToolBar):
    def __init__(self, *args, **kwargs):
        super(IpToolbar, self).__init__(*args, **kwargs)

        self.parent = args[0]

        self.init_toolbar()

    def init_toolbar(self):
        open_action = QAction(QIcon('./icons/topen.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon('./icons/tsave.png'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        rect_action = QAction('Rect', self)
        rect_action.setShortcut('Ctrl+R')
        rect_action.triggered.connect(lambda : self.parent.set_shape(IpRectangle()))

        el_action = QAction('Ell', self)
        el_action.setShortcut('Ctrl+E')
        el_action.triggered.connect(lambda : self.parent.set_shape(IpEllipse()))

        clear_action = QAction('Rest', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.parent.ip.clear)

        th_action = QAction('Thsh', self)
        th_action.setShortcut('Ctrl+T')
        th_action.triggered.connect(lambda :self.show_slider(th_action))


        self.addAction(open_action)
        self.addAction(save_action)
        self.addSeparator()

        self.addAction(rect_action)
        self.addAction(el_action)
        self.addSeparator()

        self.addAction(clear_action)
        self.addAction(th_action)

    def show_slider(self, act):
        if self.parent.img is not None:
            window = ThresholdWindow(self.parent)
            window.show()
        else:
            QMessageBox.about(self.parent, 'Info', 'load image first')

    def open_file(self, e):
        fname = QFileDialog.getOpenFileName(self, 'Open File', './')

        if fname[0]:
            self.parent.open_image(fname[0])

    def save_file(self, e):
        pass