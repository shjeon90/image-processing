import cv2
from PyQt5.QtWidgets import QToolBar, QAction, QFileDialog, QWidget, QSlider, QLabel, QDesktopWidget, QMainWindow, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from IpShape import *
from IpSlider import *

class IpToolbar(QToolBar):
    def __init__(self, parent, imagePanel, *args, **kwargs):
        super(IpToolbar, self).__init__(*args, **kwargs)

        self.parent = parent
        self.imagePanel = imagePanel

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
        rect_action.triggered.connect(lambda : self.imagePanel.set_shape(IpRectangle()))

        el_action = QAction('Ell', self)
        el_action.setShortcut('Ctrl+E')
        el_action.triggered.connect(lambda : self.imagePanel.set_shape(IpEllipse()))

        clear_action = QAction('Rest', self)
        clear_action.setShortcut('Ctrl+C')
        clear_action.triggered.connect(self.imagePanel.ip.clear)

        th_action = QAction('Thsh', self)
        th_action.setShortcut('Ctrl+T')
        th_action.triggered.connect(lambda :self.show_threshold_slide(th_action))

        hist_action = QAction('Hist', self)
        hist_action.setShortcut('Ctrl+H')
        hist_action.triggered.connect(self.imagePanel.ip.set_hist)

        gf_action = QAction('GF', self)
        gf_action.setShortcut('Ctrl+G')
        gf_action.triggered.connect(self.imagePanel.ip.set_gaussian_filter)

        bif_action = QAction('BiF', self)
        bif_action.setShortcut('Ctrl+B')
        bif_action.triggered.connect(self.imagePanel.ip.set_bilateral_filter)

        lf_action = QAction('Lap', self)
        lf_action.setShortcut('Ctrl+L')
        lf_action.triggered.connect(self.imagePanel.ip.set_laplacian_filter)

        scale_action = QAction('Scale', self)
        scale_action.triggered.connect(lambda : self.show_scale_slide(scale_action))

        rotate_action = QAction('Rotate', self)
        rotate_action.triggered.connect(lambda :self.show_rotate_dial(rotate_action))

        reflect_action = QAction('Reflect', self)
        reflect_action.triggered.connect(self.imagePanel.ip.reflect_image)

        perspective_action = QAction('Pers', self)
        perspective_action.triggered.connect(self.imagePanel.set_perspective)

        harris_action = QAction('Harris', self)
        harris_action.triggered.connect(self.imagePanel.ip.harris_corner_detect)

        fast_action = QAction('FAST', self)
        fast_action.triggered.connect(self.imagePanel.ip.fast_feature_detect)

        blob_action = QAction('BLOB', self)
        blob_action.triggered.connect(self.imagePanel.ip.blob_detect)

        orb_action = QAction('ORB', self)
        orb_action.triggered.connect(self.imagePanel.ip.orb_descriptor)

        featmat_action = QAction('FeatMat', self)
        featmat_action.triggered.connect(self.open_template_file)

        self.addAction(open_action)
        self.addAction(save_action)
        self.addSeparator()

        self.addAction(rect_action)
        self.addAction(el_action)
        self.addSeparator()

        self.addAction(clear_action)
        self.addAction(th_action)
        self.addAction(hist_action)
        self.addSeparator()

        self.addAction(gf_action)
        self.addAction(bif_action)
        self.addAction(lf_action)
        self.addSeparator()

        self.addAction(scale_action)
        self.addAction(rotate_action)
        self.addAction(reflect_action)
        self.addAction(perspective_action)
        self.addSeparator()

        self.addAction(harris_action)
        self.addAction(fast_action)
        self.addAction(blob_action)
        self.addAction(orb_action)
        self.addAction(featmat_action)

    def show_threshold_slide(self, act):
        if self.imagePanel.img is not None:
            window = ThresholdWindow(self.parent, self.imagePanel)
            window.show()
        else:
            QMessageBox.about(self.parent, 'Info', 'load image first')

    def show_scale_slide(self, act):
        if self.imagePanel.img is not None:
            window = ScaleWindow(self.parent, self.imagePanel)
            window.show()
        else:
            QMessageBox.about(self.parent, 'Info', 'load image first')

    def show_rotate_dial(self, act):
        if self.imagePanel.img is not None:
            window = RotateWindow(self.parent, self.imagePanel)
            window.show()
        else:
            QMessageBox.about(self.parent, 'Info', 'load image first')

    def open_file(self, e):
        fname = QFileDialog.getOpenFileName(self, 'Open File', './')

        if fname[0]:
            self.imagePanel.open_image(fname[0])

    def open_template_file(self):
        if self.imagePanel.img is not None:
            fname = QFileDialog.getOpenFileName(self, 'Open Template File', './')
            if fname[0]:
                img_temp = cv2.imread(fname[0], cv2.IMREAD_GRAYSCALE)
                self.imagePanel.ip.feature_match(img_temp)
        else:
            QMessageBox.about(self.parent, 'Info', 'load image first')

    def save_file(self, e):
        pass