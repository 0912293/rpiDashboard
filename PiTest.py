from guizero import App, Text, TextBox, PushButton, Slider, Picture
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, uic
from datetime import time

class mainUI(QWidget):
    def __init__(self):
        super(mainUI, self).__init__()
        qbtn.clicked(QtCore.QCoreApplication.quit)
        self.initUI()

    def initUI(self):
        self.showFullScreen()

        qbtn = QPushButton('Quit')
        qbtn.move(5, 5)
        self.button = qbtn
        qbtn.show()


def main():
    app = QApplication(sys.argv)
    window = mainUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

web = QApplication(sys.argv)
view = QWebEngineView()
view.resize(1920, 1080)
view.setUrl(QUrl("http://0912293.github.io"))
view.show()
web.exec()

'''
def print_msg():
    text.value = textbox.value


def change_text_size(slider_value):
    text.size = slider_value


app = App("Hello World")

text = Text(app, text="Hello World!", size=40, font="Arial", color="#000000")

textbox = TextBox(app, width=40)
update_text = PushButton(app, command=print_msg, text="Display my msg")
text_size = Slider(app, command=change_text_size, start=10, end=50, horizontal=True)

app.display()'''