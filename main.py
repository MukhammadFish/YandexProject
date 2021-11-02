# Импортирование библиотек и модулей
import sqlite3
import sys
import requests
import datetime

from PyQt5 import uic, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from PyQt5.QtSql import *

# Обьявление переменных
data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
count_balance = 0
count_balance_round = 0
number_dollar = data['Valute']['USD']['Value']
dt_now = datetime.datetime.now()
value_id_income = 0
value_id_expenses = 0


class MainForm(QMainWindow):
    def __init__(self):
        global count_balance
        global count_balance_round
        super().__init__()
        uic.loadUi('UI_Files/Main_Window.ui', self)
        self.initUI()

    def initUI(self):
        self.label_2.setText(str(count_balance_round) + ' руб')
        self.setWindowTitle('Анализатор')
        self.setWindowIcon(QIcon('Image_Icon/Icon_Main_Window.jpg'))

        # Соединения с методами
        self.pushButton_3.clicked.connect(self.open_income_form)
        self.pushButton_4.clicked.connect(self.open_expenses_form)
        self.pushButton_5.clicked.connect(self.open_convert_form)
        self.pushButton_2.clicked.connect(self.open_income_story_form)
        self.pushButton.clicked.connect(self.open_expenses_story_form)

    # Метод для открытия окна внесения дохода
    def open_income_form(self):
        self.income_form = IncomeForm()
        self.income_form.show()

    # Метод для открытия окна внесения вычета
    def open_expenses_form(self):
        self.expenses_form = ExpensesForm()
        self.expenses_form.show()

    # Метод для изменения баланса
    def change_balance(self):
        self.label_2.setText(str(count_balance_round) + ' руб')

    # Метод для открытия окна конвертирования
    def open_convert_form(self):
        self.convert_form = ConvertForm()
        self.convert_form.show()

    # Метод для открытия окна истории дохода
    def open_income_story_form(self):
        self.income_story_form = IncomeStoryForm()
        self.income_story_form.show()

    # Метод для открытия окна истории дохода
    def open_expenses_story_form(self):
        self.expenses_story_form = ExpensesStoryForm()
        self.expenses_story_form.show()


class IncomeForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_Files/Dependent_Window_Income.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить в бюджет')
        self.setWindowIcon(QIcon('Image_Icon/Icon_Income_Window.png'))

        # Соединения с методами
        self.pushButton.clicked.connect(self.ok_close_form)
        self.pushButton_2.clicked.connect(self.cancel_close_form)

    def ok_close_form(self):
        global count_balance
        global count_balance_round
        global dt_now
        global value_id_income

        try:
            # Обьявление локальных переменных
            list_data_income = []
            data_all = []

            # Подключение и создание курсора
            con = sqlite3.connect("MyBD.sqlite")
            cur = con.cursor()

            value_id_income += 1
            count_balance += float(self.lineEdit.text())
            count_balance_round = round(count_balance, 2)
            ex.change_balance()

            # Обновление данных для ввода в таблицу БД
            data_all.append(value_id_income)
            data_all.append(float(self.lineEdit.text()))
            data_all.append(self.comboBox.currentText())
            data_all.append(dt_now)
            list_data_income.append(tuple(data_all))

            # Ввод изменений, выход из БД и окна
            cur.executemany("INSERT INTO Income_Story(id, Total, Category, Date) VALUES (?, ?, ?, ?)", list_data_income)
            con.commit()
            con.close()
            self.close()
        except ValueError:
            self.label_3.setStyleSheet("color: rgb(250, 0, 0)")
            self.label_3.setFont(QtGui.QFont('Times', 14, QtGui.QFont.Bold))
            self.label_3.adjustSize()
            self.label_3.setText('Некорректная сумма')

    def cancel_close_form(self):
        self.close()


class ExpensesForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_Files/Dependent_Window_Deduction.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Вычесть с бюджета')
        self.setWindowIcon(QIcon('Image_Icon/Icon_Deduction_Window.png'))

        # Соединение с методами
        self.pushButton.clicked.connect(self.ok_close_form)
        self.pushButton_2.clicked.connect(self.cancel_close_form)

    def ok_close_form(self):
        global count_balance
        global count_balance_round
        global value_id_expenses

        try:
            # Обьявление локальных переменных
            data_all = []
            list_data_expenses = []

            # Подключение и создание курсора БД
            con = sqlite3.connect("MyBD.sqlite")
            cur = con.cursor()

            value_id_expenses += 1
            count_balance -= float(self.lineEdit.text())
            count_balance_round = round(count_balance, 2)
            ex.change_balance()

            # Обновление данных для ввода в таблицу БД
            data_all.append(value_id_expenses)
            data_all.append(float(self.lineEdit.text()))
            data_all.append(self.comboBox.currentText())
            data_all.append(dt_now)
            list_data_expenses.append(tuple(data_all))

            # Ввод изменений, выход из БД и окна
            cur.executemany("INSERT INTO Expenses_Story(id, Total, Category, Date) VALUES (?, ?, ?, ?)",
                            list_data_expenses)
            con.commit()
            con.close()
            self.close()
        except ValueError:
            self.label_3.setStyleSheet("color: rgb(250, 0, 0)")
            self.label_3.setFont(QtGui.QFont('Times', 14, QtGui.QFont.Bold))
            self.label_3.adjustSize()
            self.label_3.setText('Некорректная сумма')

    def cancel_close_form(self):
        self.close()


class ConvertForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_Files/Dependent_Window_Conventor.ui', self)
        self.initUI()

    def initUI(self):
        self.convert_balance = 0

        self.lineEdit_2.setReadOnly(True)
        self.setWindowTitle('Конвентор')
        self.setWindowIcon(QIcon('Image_Icon/Icon_Convert_Window.jpg'))

        # Соединение с методами
        self.pushButton_2.clicked.connect(self.add_in_balance)
        self.pushButton_3.clicked.connect(self.cancel_close_form)
        self.pushButton.clicked.connect(self.convert_money)

    def cancel_close_form(self):
        self.close()

    def convert_money(self):
        global number_dollar

        if len(self.lineEdit.text()) != 0:
            try:
                self.convert_balance = round(float(self.lineEdit.text()) * number_dollar, 2)
                self.lineEdit_2.setText(str(self.convert_balance))
            except ValueError:
                self.label_4.setStyleSheet("color: rgb(250, 0, 0)")
                self.label_4.setFont(QtGui.QFont('Times', 12, QtGui.QFont.Bold))
                self.label_4.adjustSize()
                self.label_4.setText('Некорректная сумма')

    def add_in_balance(self):
        global count_balance
        global count_balance_round
        global data
        global value_id_income

        # Обьявление локальных переменных
        list_data_expenses = []
        data_all = []

        # Создание подключение и курсора БД
        con = sqlite3.connect("MyBD.sqlite")
        cur = con.cursor()

        # Изменение данных для ввода в таблицу БД
        value_id_income += 1
        count_balance += self.convert_balance
        count_balance_round = round(count_balance, 2)
        data_all.append(value_id_income)
        data_all.append(float(self.lineEdit_2.text()))
        data_all.append('Конвертация(Доллар)')
        data_all.append(dt_now)
        list_data_expenses.append(tuple(data_all))

        # Ввод изменений, выход из БД и окна
        cur.executemany("INSERT INTO Income_Story(id, Total, Category, Date) VALUES (?, ?, ?, ?)",
                        list_data_expenses)
        con.commit()
        con.close()
        self.close()
        ex.change_balance()


class IncomeStoryForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_Files/Window_Income_Story.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('История доходов')
        self.setWindowIcon(QIcon('Image_Icon/Icon_Story.png'))

        self.pushButton_3.clicked.connect(self.cancel_close_form)

        # Открытие БД
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('MyBD.sqlite')
        self.db.open()

        # Отображение таблицы в виджет
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('Income_Story')
        self.model.select()
        self.tableView.setModel(self.model)

    def cancel_close_form(self):
        self.close()


class ExpensesStoryForm(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('UI_Files/Window_Expenses_Story.ui', self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('История расходов')
        self.setWindowIcon(QIcon('Image_Icon/Icon_Story.png'))
        self.pushButton.clicked.connect(self.cancel_close_form)

        # Открытие БД
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('MyBD.sqlite')
        self.db.open()

        # Отображение таблицы в виджет
        self.model = QSqlTableModel(self, self.db)
        self.model.setTable('Expenses_Story')
        self.model.select()
        self.tableView.setModel(self.model)

    def cancel_close_form(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainForm()
    ex.show()
    sys.exit(app.exec())