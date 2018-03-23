from designer import homeScreen
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QMessageBox,QTableWidgetItem
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from PyQt5.QtCore import Qt
from PyQt5 import QtCore, QtGui, uic
from datetime import time
import urllib.request
import json


class MainUi(QMainWindow, homeScreen.Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainUi, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.popTable()

    def initUI(self):
        QMainWindow.showFullScreen(self)
        self.pushButton.setToolTip("button 1")
        self.pushButton_2.setToolTip("button 2")
        self.pushButton_2.clicked.connect(self.buttonClicked)
        self.label.setToolTip("Label 1")
        self.label_2.setToolTip("Label 2")
        self.pushButton.setText("Schedule")
        self.pushButton.clicked.connect(self.buttonClicked)
        self.pushButton_2.setText("Defects")
        self.label.setText("capacity")
        self.label_2.setText("temp")

    def popTable(self):
        for i in range(15):
            self.tableWidget.setItem(i,0, QTableWidgetItem(str(i+1)))
        contents = urllib.request.urlopen(
            "http://markb.pythonanywhere.com/getdata").read()  # b'{"Reservation": {"ReservationID": 10, "TimeSlotFrom": 2, "TimeSlotTo": 3, "TimeFrom": "10:50", "TimeTo": "11:40", "Date": "12-03-2003", "Username": "OmarA", "Lesson": "ICTLAB", "Room": "WN4.101"}}'
        data = json.loads(contents.decode('utf-8'))
        print(json.dumps(data, indent=4, sort_keys=True))
        self.insertTable(data)

    def insertTable(self, data):
        self.tableWidget.setItem(int(data["Reservation"]["TimeSlotFrom"]), 1, QTableWidgetItem(
            str(data["Reservation"]["TimeFrom"]) + " " + str(data["Reservation"]["TimeTo"]) + " " + str(
                data["Reservation"]["Username"]) + " " + str(data["Reservation"]["Lesson"])))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def closeEvent(self):
        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()

    def keyPressEvent(self, e):

        if e.key() == Qt.Key_Escape:
            self.closeEvent()

    def mouseMoveEvent(self, e):
        x = e.x()
        y = e.y()

        text = "x: {0},  y: {1}".format(x, y)
        self.label.setText(text)

    def buttonClicked(self):
        sender = self.sender()
        if sender is self.pushButton:
            self.label_2.setText("REEE")
        elif sender is self.pushButton_2:
            self.label.setText(sender.text() + ' was pressed')


def main():
    app = QApplication(sys.argv)
    main = MainUi()
    main.show()
    app.exec_()


if __name__ == '__main__':
    main()