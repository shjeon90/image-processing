import sys
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QAction, QMainWindow, QApplication, QWidget
from PyQt5.QtGui import QPixmap, QPainter

class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.image = QPixmap("student id card-front.jpg")
        self.setFixedSize(self.image.size())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        newAct = QAction('New', self)
        self.toolbar = self.addToolBar('Remove')
        self.toolbar.addAction(newAct)
        self.setCentralWidget(Widget())
        self.setFixedSize(self.sizeHint())
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainMenu = Menu()
    sys.exit(app.exec_())