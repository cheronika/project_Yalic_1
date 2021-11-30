import sqlite3
import sys
from random import randint

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.score_number = 0
        self.subject_number = 0
        self.game_mode = 0
        self.what_is = 'Что находится на карте под номером'
        uic.loadUi("дизайн.ui", self)
        self.initUI()

    def initUI(self):
        self.setGeometry(400, 400, 800, 800)
        self.stackedWidget.setCurrentIndex(0)
        self.send_mode_choice.clicked.connect(self.game_mode)
        self.send_rus.clicked.connect(self.send)
        self.idk_1.clicked.connect(self.idk)

    def game_mode(self):
        self.score_number = 0
        if self.russian_subjects.isChecked():
            self.game_mode = 1
            self.stackedWidget.setCurrentIndex(1)
            self.pixmap = QPixmap('карта.jpg')
            self.image = QLabel(self)
            self.image.setPixmap(self.pixmap)
            # with open('subjects.csv', encoding='utf-8', newline='') as csvfile:
            # self.reader = csv.DictReader(csvfile, delimiter=';', quotechar='"')
            f = open('subjects.txt', mode='rt', encoding='UTF-8')
            self.data = f.read().split("\n")
            self.subject_number = randint(1, 23)
            while self.subject_number == 19:
                self.subject_number = randint(1, 23)
            self.now_subject = self.data[self.subject_number - 1].split(';')[1]
            print(self.now_subject)
            self.ex_1.setText(self.what_is + str(self.subject_number) + '?')
        elif self.europe_countries.isChecked():
            self.game_mode = self.stackedWidget.currentIndex()
            self.stackedWidget.setCurrentIndex(2)

    def send(self):
        print(repr(self.answer_1.text().lower()))
        print(repr(self.now_subject))
        print(repr(self.answer_1.text().lower() == self.now_subject))
        if self.answer_1.text().lower() == self.now_subject:
            self.score_number += 1
            self.score_lcd.display(self.score_number)
            self.wrong_answer.setText('')
            self.subject_number = randint(1, 22)
            while self.subject_number == 19:
                self.subject_number = randint(1, 23)
            self.now_subject = self.data[self.subject_number - 1].split(';')[1]
            self.ex_1.setText(self.what_is + str(self.subject_number) + '?')
        else:
            self.wrong_answer.setText('Неправильный ответ. Попробуйте еще раз.')

    def idk(self):
        con = sqlite3.connect('tries.sql.db3')
        cur = con.cursor()
        result = con.execute('''SELECT COUNT (*) FROM i_dont_know WHERE name_of_object LIKE ?''', self.now_subject).fetchone()
        print(result)
        # print(con.execute('''SELECT COUNT  FROM i_dont_know WHERE name_of_object LIKE ?''', self.now_subject))
        # if con.execute('''SELECT COUNT FROM i_dont_know WHERE name_of_object LIKE ?''', self.now_subject) == 0:
        # con.execute('''UPDATE i_dont_know SET count = count + 1 WHERE name == self.now_subject''')
        con.execute('''INSERT INTO i_dont_know(name_of_object, mode_number, count) 
            VALUES(?, ?, 1)''', (self.now_subject, self.stackedWidget.currentIndex()))
        con.commit()
        self.answer_1.setText(self.now_subject)
        self.wrong_answer.setText('Посмотрите на правильный ответ. Сейчас появится новое задание.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
