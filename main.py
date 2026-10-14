import sys

from PySide6.QtWidgets import QApplication, QDialog

from models import Session
from ui import LoginDialog, MainWindow


class App:
    @staticmethod
    def run():
        qt_app = QApplication(sys.argv)

        dialog = LoginDialog()
        if dialog.exec() != QDialog.Accepted:
            return 0

        session = Session(dialog.login)
        window = MainWindow(session)
        window.show()
        return qt_app.exec()


if __name__ == "__main__":
    sys.exit(App.run())