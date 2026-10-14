from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
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

from models import Expense, MyMap


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
        self.setDecimals(0)
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
        for row, expense in enumerate(expenses):
            self.setItem(row, 0, QTableWidgetItem(expense.title))
            self.setItem(row, 1, QTableWidgetItem(str(expense.amount)))
            self.setItem(row, 2, QTableWidgetItem(expense.category))


class MyGroupBox(QGroupBox):
    def __init__(self, title):
        super().__init__(title)
        self.setStyleSheet("font-weight: bold;")


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

    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    def check_login(self):
        text = self.edit.text().strip()
        if text == "":
            QMessageBox.warning(self, "Ошибка", "Введите логин")
        else:
            self.login = text
            self.accept()


class MainWindow(QMainWindow):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle(f"Учёт расходов - {session.login}")
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
        for title, amount, category in data:
            self.expenses.append(Expense(title, amount, category))

    def refresh(self):
        self.table.fill(self.expenses)

        total = 0
        by_category = MyMap()
        for expense in self.expenses:
            total += expense.amount
            by_category.put(expense.category, by_category.get(expense.category) + expense.amount)

        self.total_label.setText(f"Итого: {total} тг")
        self.stats_label.setText(f"По категориям: {by_category}")

    def add_expense(self):
        try:
            expense = Expense(
                self.title_edit.text(),
                int(self.amount_spin.value()),
                self.category_box.currentText(),
            )
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
