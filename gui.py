import re
import sys
from threading import Thread

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QApplication,
    QPushButton, QDesktopWidget,
    QMessageBox, QTableWidget,
    QTableWidgetItem
)

from hoper.util.history_util import get_history
from hoper.util.types import Hope

RE = re.compile(r'https?://.+\..+')


class HoperApplication(QWidget):
    _go_btn = None
    _url_input = None
    _msg_box = None
    _table = None
    _url = None

    def __init__(self):
        super().__init__()

        self.setFixedSize(500, 450)
        self.setWindowTitle('Hopper gui')

        self.init_ui()
        self.init_msg_box()

    def init_msg_box(self):
        self._msg_box = QMessageBox(self)
        self._msg_box.setWindowTitle('Error')

        font = QFont()
        font.setWeight(50)
        font.setPixelSize(15)

        label = QLabel('Bad url', self._msg_box)
        label.setFont(font)
        label.move(20, 5)

    def init_ui(self):
        font = QFont()
        font.setWeight(30)
        font.setPixelSize(15)

        label = QLabel('url:', self)
        label.move(10, 14)
        label.setFont(font)

        self._url_input = QLineEdit(self)
        self._url_input.setPlaceholderText('https://example.com')
        self._url_input.move(40, 10)
        self._url_input.setFixedSize(300, 24)

        self._go_btn = QPushButton('GO', self)
        self._go_btn.move(350, 10)
        self._go_btn.clicked.connect(self.fill_history)

        self._table = QTableWidget(0, 4, self)
        self._table.move(10, 50)
        self._table.setHorizontalHeaderLabels(['url', 'status', 'time', 'type', ])
        self._table.setFixedSize(480, 390)

    def fill_history(self):
        self._url = self._url_input.text()
        if RE.match(self._url) is None:
            self._msg_box.show()
            return

        try:
            Thread(target=self._updater, args=(self._url,), ).start()
        except Exception as e:
            print(e)

    def _updater(self, url: str):
        if url is None:
            return

        self._table.setRowCount(0)

        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0 Hoper"
        n = 0
        for row in get_history(url, user_agent=user_agent):  # type: Hope
            self._table.insertRow(n)
            self._table.setItem(n, 0, QTableWidgetItem(row.url))
            self._table.setItem(n, 1, QTableWidgetItem(str(row.status)))
            self._table.setItem(n, 2, QTableWidgetItem(str(row.time)))
            self._table.setItem(n, 3, QTableWidgetItem(row.type))

            n += 1

    def location_on_the_screen(self):
        ag = QDesktopWidget().availableGeometry()
        sg = QDesktopWidget().screenGeometry()

        me = self.geometry()
        x = ag.width() - me.width()
        y = 2 * ag.height() - sg.height() - me.height()
        self.move(int(x / 2), int(y / 2))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    covid_app = HoperApplication()
    covid_app.show()
    covid_app.location_on_the_screen()
    exit(app.exec_())
