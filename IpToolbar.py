from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog
from PyQt5.QtGui import QIcon
from IpShape import *

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

        el_action = QAction('Ellipse', self)
        el_action.setShortcut('Ctrl+E')
        el_action.triggered.connect(lambda : self.parent.set_shape(IpEllipse()))

        self.addAction(open_action)
        self.addAction(save_action)
        self.addAction(rect_action)
        self.addAction(el_action)

    def set_cur_shape(self, shape):
        print(shape)

    def open_file(self, e):
        fname = QFileDialog.getOpenFileName(self, 'Open File', './')

        if fname[0]:
            self.parent.open_image(fname[0])

    def save_file(self, e):
        pass