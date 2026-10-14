import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

class Entity(ABC):
    @abstractmethod
    def describe(self):
        pass

class Expense(Entity):
    def __init__(self, title, amount, category):
        self.title = title
        self.amount = amount
        self.category = category

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if value.strip() == "":
            raise ValueError("Введите название")
        self._title = value.strip()

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if value <= 0:
            raise ValueError("Сумма должна быть больше нуля")
        self._amount = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    def describe(self):
        return "Расход: " + self.title

    def __str__(self):
        return self.title + " - " + str(self.amount) + " тг"

    def __repr__(self):
        return "Expense(" + self.title + ")"

    def __eq__(self, other):
        return self.title == other.title and self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __hash__(self):
        return hash((self.title, self.amount))

class MyMap(Entity):
    def __init__(self):
        self.keys = []
        self.values = []

    def put(self, key, value):
        if key in self.keys:
            index = self.keys.index(key)
            self.values[index] = value
        else:
            self.keys.append(key)
            self.values.append(value)

    def get(self, key):
        if key in self.keys:
            return self.values[self.keys.index(key)]
        return 0

    def describe(self):
        return "Мой словарь"

    def __len__(self):
        return len(self.keys)

    def __contains__(self, key):
        return key in self.keys

    def __getitem__(self, key):
        return self.get(key)

    def __eq__(self, other):
        return self.keys == other.keys and self.values == other.values

    def __repr__(self):
        return "MyMap(" + str(self.keys) + ")"

    def __str__(self):
        text = ""
        for i in range(len(self.keys)):
            text = text + self.keys[i] + ": " + str(self.values[i]) + " тг;  "
        return text

class Session(Entity):
    def __init__(self, login):
        self.login = login
        self.time_in = datetime.now()
        self.time_out = None

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, value):
        self._time_in = value

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, value):
        self._time_out = value

    def describe(self):
        return "Вход пользователя " + self.login

    def save_report(self):
        self.time_out = datetime.now()
        fmt = "%d.%m.%Y %H:%M:%S"
        line = "+" + "-" * 14 + "+" + "-" * 21 + "+" + "-" * 21 + "+\n"
        file_is_new = not os.path.exists("report.txt")
        with open("report.txt", "a", encoding="utf-8") as f:
            if file_is_new:
                f.write(line)
                f.write("| " + "login".center(12) + " | " + "time_in".center(19) + " | " + "time_out".center(19) + " |\n")
                f.write(line)
            f.write("| " + self.login[:12].ljust(12) + " | " + self.time_in.strftime(fmt) + " | " + self.time_out.strftime(fmt) + " |\n")
            f.write(line)

    def __lt__(self, other):
        return self.time_in < other.time_in

    def __gt__(self, other):
        return self.time_in > other.time_in

    def __hash__(self):
        return hash((self.login, self.time_in))

    def __eq__(self, other):
        return self.login == other.login and self.time_in == other.time_in

    def __repr__(self):
        return "Session(" + self.login + ")"

    def __str__(self):
        return self.login + " вошёл в " + str(self.time_in)

class MyLabel(QLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setStyleSheet("font-size: 14px;")

class MyTitle(MyLabel):
    def __init__(self, text=""):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 22px; font-weight: bold;")

class MyTotalLabel(MyLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("font-size: 16px; font-weight: bold; color: green;")

class MyLineEdit(QLineEdit):
    def __init__(self, hint=""):
        super().__init__()
        self.setPlaceholderText(hint)

class MyButton(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setMinimumHeight(35)
        self.setStyleSheet("background: green; color: white;")

class MyComboBox(QComboBox):
    def __init__(self, items):
        super().__init__()
        self.addItems(items)

class MySpinBox(QDoubleSpinBox):
    def __init__(self):
        super().__init__()
        self.setRange(1, 10000000)
        self.setSuffix(" тг")

class MyTable(QTableWidget):
    def __init__(self):
        super().__init__(0, 3)
        self.setHorizontalHeaderLabels(["Название", "Сумма", "Категория"])
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.horizontalHeader().setStretchLastSection(True)

    def fill(self, expenses):
        self.setRowCount(len(expenses))
        for row in range(len(expenses)):
            e = expenses[row]
            self.setItem(row, 0, QTableWidgetItem(e.title))
            self.setItem(row, 1, QTableWidgetItem(str(e.amount)))
            self.setItem(row, 2, QTableWidgetItem(e.category))

class MyGroupBox(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.setStyleSheet("font-weight: bold;")

# Окно входа
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Вход")
        self.login = ""

        self.edit = MyLineEdit("Введите логин")
        self.button = MyButton("Войти")
        self.button.clicked.connect(self.check_login)

        layout = QVBoxLayout(self)
        layout.addWidget(MyTitle("Учёт расходов"))
        layout.addWidget(self.edit)
        layout.addWidget(self.button)

    def check_login(self):
        if self.edit.text().strip() == "":
            QMessageBox.warning(self, "Ошибка", "Введите логин")
        else:
            self.login = self.edit.text().strip()
            self.accept()

class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Учёт расходов - " + session.login)
        self.resize(600, 550)

        self.categories = ["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье"]
        self.expenses = []
        self.make_demo_expenses()

        self.title_edit = MyLineEdit("Например: Продукты")
        self.amount_spin = MySpinBox()
        self.category_box = MyComboBox(self.categories)
        add_button = MyButton("Добавить")
        add_button.clicked.connect(self.add_expense)

        form_box = MyGroupBox("Новый расход")
        form = QFormLayout(form_box)
        form.addRow("Название:", self.title_edit)
        form.addRow("Сумма:", self.amount_spin)
        form.addRow("Категория:", self.category_box)
        form.addRow("", add_button)

        self.table = MyTable()
        delete_button = MyButton("Удалить выбранный")
        delete_button.clicked.connect(self.delete_expense)
        self.total_label = MyTotalLabel()
        self.stats_label = MyLabel()

        center = QWidget()
        layout = QVBoxLayout(center)
        layout.addWidget(MyTitle("Мои расходы"))
        layout.addWidget(form_box)
        layout.addWidget(self.table)
        layout.addWidget(delete_button)
        layout.addWidget(self.total_label)
        layout.addWidget(self.stats_label)
        self.setCentralWidget(center)

        self.refresh()

    def make_demo_expenses(self):
        data = [
            ("Продукты", 60000, "Еда"),
            ("Кафе", 3000, "Еда"),
            ("Автобус", 10000, "Транспорт"),
            ("Такси", 20000, "Транспорт"),
            ("Кино", 5000, "Развлечения"),
            ("Подписка", 20000, "Развлечения"),
            ("Аренда", 200000, "Жильё"),
            ("Интернет", 23000, "Жильё"),
            ("Аптека", 20000, "Здоровье"),
            ("Обед", 70000, "Еда"),
        ]
        for item in data:
            expense = Expense(item[0], item[1], item[2])
            self.expenses.append(expense)

    def refresh(self):
        self.table.fill(self.expenses)

        total = 0
        by_category = MyMap()
        for e in self.expenses:
            total = total + e.amount
            by_category.put(e.category, by_category.get(e.category) + e.amount)

        self.total_label.setText("Итого: " + str(total) + " тг")
        self.stats_label.setText("По категориям: " + str(by_category))

    def add_expense(self):
        try:
            expense = Expense(self.title_edit.text(), self.amount_spin.value(), self.category_box.currentText())
        except ValueError as error:
            QMessageBox.warning(self, "Ошибка", str(error))
            return
        self.expenses.append(expense)
        self.title_edit.clear()
        self.refresh()

    def delete_expense(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Удаление", "Выберите строку")
            return
        self.expenses.pop(row)
        self.refresh()

    def closeEvent(self, event):
        self.session.save_report()
        event.accept()

# Запустить программу
def main():
    qt_app = QApplication(sys.argv)

    dialog = LoginDialog()
    if dialog.exec() != QDialog.Accepted:
        return 0

    session = Session(dialog.login)
    window = MainWindow(session)
    window.show()
    return qt_app.exec()

if __name__ == "__main__":
    sys.exit(main())