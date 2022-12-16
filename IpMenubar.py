import cv2
from PyQt5.QtWidgets import QMenuBar, QAction, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from IpSlider import *

class IpMenubar(QMenuBar):
    def __init__(self, parent, imagePanel, *args, **kwargs):
        super(IpMenubar, self).__init__(*args, **kwargs)

        self.parent = parent
        self.imagePanel = imagePanel

        self.init_menubar()

    def init_menubar(self):
        open_action = QAction(QIcon('./icons/topen.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)

        save_action = QAction(QIcon('./icons/tsave.png'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)

        th_action = QAction('Thsh', self)
        th_action.triggered.connect(lambda: self.show_threshold_slide(th_action))

        hist_action = QAction('Hist', self)
        hist_action.triggered.connect(self.imagePanel.ip.set_hist)

        gf_action = QAction('GF', self)
        gf_action.triggered.connect(self.imagePanel.ip.set_gaussian_filter)

        bif_action = QAction('BiF', self)
        bif_action.triggered.connect(self.imagePanel.ip.set_bilateral_filter)

        lf_action = QAction('Lap', self)
        lf_action.triggered.connect(self.imagePanel.ip.set_laplacian_filter)

        scale_action = QAction('Scale', self)
        scale_action.triggered.connect(lambda: self.show_scale_slide(scale_action))

        rotate_action = QAction('Rotate', self)
        rotate_action.triggered.connect(lambda: self.show_rotate_dial(rotate_action))

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


        file_menu = self.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)

        threshold_menu = self.addMenu('&Threshold')
        threshold_menu.addAction(th_action)

        histogram_menu = self.addMenu('&Histogram')
        histogram_menu.addAction(hist_action)

        filter_menu = self.addMenu('Filter')
        filter_menu.addAction(gf_action)
        filter_menu.addAction(bif_action)
        filter_menu.addAction(lf_action)

        transform_menu = self.addMenu('Transform')
        transform_menu.addAction(scale_action)
        transform_menu.addAction(rotate_action)
        transform_menu.addAction(reflect_action)
        transform_menu.addAction(perspective_action)

        feature_menu = self.addMenu('Feature')
        feature_menu.addAction(harris_action)
        feature_menu.addAction(fast_action)
        feature_menu.addAction(blob_action)
        feature_menu.addAction(featmat_action)


    def open_file(self, e):
        fname = QFileDialog.getOpenFileName(self, 'Open File', './')

        if fname[0]:
            self.imagePanel.open_image(fname[0])

    def save_file(self, e):
        pass

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

    def open_template_file(self):
        if self.imagePanel.img is not None:
            fname = QFileDialog.getOpenFileName(self, 'Open Template File', './')
            if fname[0]:
                img_temp = cv2.imread(fname[0], cv2.IMREAD_GRAYSCALE)
                self.imagePanel.ip.feature_match(img_temp)
        else:
            QMessageBox.about(self.parent, 'Info', 'load image first')