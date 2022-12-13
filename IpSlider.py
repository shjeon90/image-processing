from PyQt5.QtWidgets import QMainWindow, QSlider, QDial
from PyQt5.QtCore import Qt

class ThresholdWindow(QMainWindow):
    def __init__(self, parent, imagePanel, *args, **kwargs):
        super(ThresholdWindow, self).__init__(parent, *args, **kwargs)

        self.parent = parent
        self.imagePanel = imagePanel

        self.init()

    def init(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 255)
        slider.setSingleStep(1)
        slider.setValue(0)

        slider.valueChanged.connect(self.on_value_changed)

        self.setWindowTitle('Threshold:')

    def on_value_changed(self, e):
        self.imagePanel.ip.set_threshold(e)

class ScaleWindow(QMainWindow):
    def __init__(self, parent, imagePanel, *args, **kwargs):
        super(ScaleWindow, self).__init__(parent, *args, **kwargs)

        self.parent = parent
        self.imagePanel = imagePanel

        self.init()

    def init(self):
        slider = QSlider(Qt.Horizontal, self)
        slider.setRange(0, 255)
        slider.setSingleStep(1)
        slider.setValue(128)

        slider.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, e):
        self.imagePanel.ip.scale_image(e)

class RotateWindow(QMainWindow):
    def __init__(self, parent, imagePanel, *args, **kwargs):
        super(RotateWindow, self).__init__(parent, *args, **kwargs)

        self.parent = parent
        self.imagePanel = imagePanel

        self.init()

    def init(self):
        dial = QDial(self)
        dial.setRange(0, 360)
        dial.setSingleStep(1)
        dial.setValue(0)

        dial.valueChanged.connect(self.on_value_changed)

    def on_value_changed(self, e):
        self.imagePanel.ip.rotate_image(e)
