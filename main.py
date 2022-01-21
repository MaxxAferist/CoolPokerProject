import pygame
import sys
import sqlite3
from menu import *
from Window_reg import Window_reg
from Window_start import Window_start
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *


class MainWindow(QMainWindow, Window_start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.go_reg)

    def start(self):
        pygame.init()
        start_menu = Menu()
        start_menu.run()
        con = sqlite3.connect("data//User_list.db")
        cur = con.cursor()
        User = self.lineEdit.text()
        Pass = self.lineEdit_2.text()
        result = cur.execute(f"""SELECT id FROM Users
                                        WHERE User = '{User}' and Password = '{Pass}'""").fetchone()

        if result != None:
            pygame.init()
            start_menu = Menu()
            start_menu.run()
        else:
            self.statusbar.showMessage('Пользователя несуществует')

        con.close()

    def go_reg(self):
        ex1 = Reg_Window()
        ex1.show()
        self.ex = Reg_Window()
        self.ex.show()
        self.close()


class Reg_Window(QMainWindow, Window_reg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.added)

    def added(self):
        con = sqlite3.connect("data//User_list.db")
        cur = con.cursor()
        User = self.lineEdit.text()
        Pass = self.lineEdit_2.text()
        cur.execute(f"""INSERT INTO Users(User,Password,Count) VALUES('{User}','{Pass}', 1000)""").fetchone()

        con.commit()
        con.close()

        self.ex = MainWindow()
        self.ex.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
