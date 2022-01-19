import pygame
import sys
from menu import *
from Window_reg import Window_reg
from Window_start import Window_start
from PyQt5.QtWidgets import QApplication, QMainWindow


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

    def go_reg(self):
        ex1 = Reg_Window()
        ex1.show()


class Reg_Window(QMainWindow, Window_reg):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
