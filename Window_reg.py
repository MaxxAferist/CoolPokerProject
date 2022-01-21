from PyQt5 import QtCore, QtGui, QtWidgets
from ctypes import *

KOEF = windll.user32.GetSystemMetrics(0) / 1920


class Window_reg(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 250)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 480, 50))
        self.label.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(220, 60, 150, 25))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(220, 100, 150, 25))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 60, 181, 25))
        self.label_2.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 100, 181, 25))
        self.label_3.setStyleSheet("font: 25 16pt \"Microsoft YaHei Light\";")
        self.label_3.setObjectName("label_3")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(290, 140, 191, 41))
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", f"<html><head/><body><p align=\"center\"><span style=\" font-size:{22 * KOEF}pt;\">Регистрация</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", f"<html><head/><body><p align=\"right\"><span style=\" font-size:{16 * KOEF}pt;\">Логин</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", f"<html><head/><body><p align=\"right\"><span style=\" font-size:{16 * KOEF}pt;\">Пароль</span></p></body></html>"))
        self.pushButton.setText(_translate("MainWindow", "Зарегистрироваться"))
