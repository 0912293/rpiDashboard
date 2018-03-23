import uiTest
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, uic
from datetime import time

class ExampleApp(QMainWindow, uiTest.Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()