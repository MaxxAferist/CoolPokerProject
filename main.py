import pygame
import sys
import sqlite3
from menu import *
from Window_reg import Window_reg
from Window_start import Window_start
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import *
import datetime as DT
import math


class MainWindow(QMainWindow, Window_start):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.start)
        self.pushButton_2.clicked.connect(self.go_reg)

    def start(self):
        pygame.init()
        con = sqlite3.connect("data//User_list.db")
        cur = con.cursor()
        User = self.lineEdit.text()
        Pass = self.lineEdit_2.text()
        result = cur.execute(f"""SELECT Count, Lust_online FROM Users
                                        WHERE User = '{User}' and Password = '{Pass}'""").fetchone()

        if result != None:
            count = result[0]
            pygame.init()
            time_format_1 = "%Y-%m-%d %H:%M:%S"
            time_format_2 = "%H:%M:%S"
            now = DT.datetime.now(DT.timezone.utc).astimezone()
            now = DT.datetime.strptime(f"{now:{time_format_1}}", time_format_1)
            last_time = DT.datetime.strptime(result[1], time_format_1)
            hours = (DT.datetime.strptime(f"{now:{time_format_1}}", time_format_1) - last_time).total_seconds() / 3600
            time = DT.datetime.strptime(f"{now:{time_format_1}}", time_format_1) - last_time
            time_timer = DT.datetime.strptime('4:00:00', time_format_2) - DT.datetime.strptime(f'{time}', time_format_2)
            if hours >= 4:
                n = math.trunc(hours / 4)
                count += 400 * n
            while hours >= 4:
                print(hours)
                now = DT.datetime.now(DT.timezone.utc).astimezone()
                now = DT.datetime.strptime(f"{now:{time_format_1}}", time_format_1)
                last_time = last_time + DT.timedelta(hours=4)
                hours = (DT.datetime.strptime(f"{now:{time_format_1}}",
                                              time_format_1) - last_time).total_seconds() / 3600
                time = DT.datetime.strptime(f"{now:{time_format_1}}", time_format_1) - last_time
                time_timer = DT.datetime.strptime('4:00:00', time_format_2) - DT.datetime.strptime(f'{time}',
                                                                                                   time_format_2)

                cur.execute(f"""UPDATE Users
SET 
    Lust_online = '{last_time}'
WHERE User = '{User}'""")
                con.commit()

            start_menu = Menu(count, User)
            start_menu.run()
            self.close()
        else:
            self.statusbar.showMessage('Пользователя несуществует')

        con.close()

    def go_reg(self):
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
        now = DT.datetime.now(DT.timezone.utc).astimezone()
        time_format_1 = "%Y-%m-%d %H:%M:%S"
        now = DT.datetime.strptime(f"{now:{time_format_1}}", time_format_1)
        cur.execute(f"""INSERT INTO Users(User,Password,Count, Lust_online) VALUES('{User}','{Pass}', 1000, '{now}')""")

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
