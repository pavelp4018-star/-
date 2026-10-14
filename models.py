import os
from abc import ABC, abstractmethod
from datetime import datetime

DATE_FORMAT = "%d.%m.%Y %H:%M:%S"
REPORT_FILE = "report.txt"

BORDER = "+" + "-" * 58 + "+\n"
SEPARATOR = "|" + "-" * 14 + "|" + "-" * 21 + "|" + "-" * 21 + "|\n"
HEADER = f"| {'login':^12} | {'time_in':^19} | {'time_out':^19} |\n"


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
        return f"Расход: {self.title}"

    def __str__(self):
        return f"{self.title} - {self.amount} тг"

    def __repr__(self):
        return f"Expense({self.title!r}, {self.amount}, {self.category!r})"

    def __eq__(self, other):
        if not isinstance(other, Expense):
            return False
        return self.title == other.title and self.amount == other.amount

    def __lt__(self, other):
        return self.amount < other.amount

    def __gt__(self, other):
        return self.amount > other.amount

    def __hash__(self):
        return hash((self.title, self.amount))


class MyMap(Entity):
    """Свой словарь: ключи и значения лежат в двух списках."""

    def __init__(self):
        self.keys = []
        self.values = []

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, value):
        self._keys = value

    @property
    def values(self):
        return self._values

    @values.setter
    def values(self, value):
        self._values = value

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
        if not isinstance(other, MyMap):
            return False
        return self.keys == other.keys and self.values == other.values

    def __lt__(self, other):
        return len(self) < len(other)

    def __gt__(self, other):
        return len(self) > len(other)

    def __repr__(self):
        return f"MyMap({self.keys})"

    def __str__(self):
        parts = []
        for i in range(len(self.keys)):
            parts.append(f"{self.keys[i]}: {self.values[i]} тг")
        return ";  ".join(parts)


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
        return f"Вход пользователя {self.login}"

    def save_report(self):
        self.time_out = datetime.now()
        row = (
            f"| {self.login[:12]:<12} "
            f"| {self.time_in.strftime(DATE_FORMAT)} "
            f"| {self.time_out.strftime(DATE_FORMAT)} |\n"
        )

        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            lines = lines[:-1]  # убираем нижнюю границу, чтобы дописать строку
        else:
            lines = [BORDER, HEADER, SEPARATOR]

        lines.append(row)
        lines.append(BORDER)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def __lt__(self, other):
        return self.time_in < other.time_in

    def __gt__(self, other):
        return self.time_in > other.time_in

    def __hash__(self):
        return hash((self.login, self.time_in))

    def __eq__(self, other):
        if not isinstance(other, Session):
            return False
        return self.login == other.login and self.time_in == other.time_in

    def __repr__(self):
        return f"Session({self.login!r})"

    def __str__(self):
        return f"{self.login} вошёл в {self.time_in}"
