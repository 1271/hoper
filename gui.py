import re
import sys

from PyQt5.QtCore import QObject, QThread, pyqtSlot, pyqtSignal
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QApplication,
    QPushButton, QDesktopWidget,
    QMessageBox, QTableWidget,
    QTableWidgetItem, QVBoxLayout,
    QGroupBox, QGridLayout
)

from hoper.util.history_util import get_history
from hoper.util.types import Hope

RE = re.compile(r'https?://.+\..+')


class Worker(QObject):
    emitter = pyqtSignal(int, dict)
    emitter_done = pyqtSignal(bool)

    @pyqtSlot(str)
    def fill_data(self, url: str):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0 Hoper"
        n = 0

        try:
            for row in get_history(url, user_agent=user_agent):  # type: Hope
                self.emitter.emit(n, {
                    'type': row.type,
                    'url': row.url,
                    'status': row.status,
                    'time': row.time,
                    'headers': row.headers,
                    'hook': row.hook,
                    'original_url': row.original_url,
                })
                n += 1

        except Exception:
            pass

        self.emitter_done.emit(True)


class HoperApplication(QWidget):
    __worker = None
    __worker_thread = None
    _emitter = pyqtSignal(str)

    _window_title = 'Hopper gui'
    _go_btn = None
    _url_input = None
    _msg_box = None
    _table = None
    _url = None

    _height = 700
    _width = 750

    _success_fill = True

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, self._height, self._width)
        self.setMinimumSize(400, 400)
        self.setWindowTitle(self._window_title)

        self.init_ui()
        self.init_msg_box()
        self.init_worker()

    def init_worker(self):
        self.__worker = Worker()
        self.__worker_thread = QThread()

        self.__worker.emitter.connect(self.new_result)
        self.__worker.emitter_done.connect(self.all_done)
        self._emitter.connect(self.__worker.fill_data)

        self.__worker.moveToThread(self.__worker_thread)
        self.__worker_thread.start()

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

        label = QLabel('url:')
        label.setFont(font)
        label.move(0, -20)

        self._url_input = QLineEdit()
        self._url_input.setPlaceholderText('https://example.com')
        self._url_input.move(0, -20)

        self._go_btn = QPushButton('GO')
        self._go_btn.clicked.connect(self.fill_history)
        self._go_btn.move(0, -20)

        window_layout = QVBoxLayout()

        horizontal_group_box_top = QGroupBox()
        layout_top = QGridLayout()
        layout_top.setColumnStretch(1, 1)
        layout_top.addWidget(label, 0, 0)
        layout_top.addWidget(self._url_input, 0, 1)
        layout_top.addWidget(self._go_btn, 0, 2)
        horizontal_group_box_top.setLayout(layout_top)

        self._table = QTableWidget(0, 3)
        self._table.setColumnWidth(0, 400)
        self._table.setHorizontalHeaderLabels(['url', 'status', 'time',])

        horizontal_group_box_center = QGroupBox()
        layout_center = QGridLayout()
        layout_center.setColumnStretch(0, 1)
        layout_center.addWidget(self._table)
        horizontal_group_box_center.setLayout(layout_center)

        window_layout.addWidget(horizontal_group_box_top)
        window_layout.addWidget(horizontal_group_box_center)

        self.setLayout(window_layout)

    def fill_history(self):
        self._url = self._url_input.text()
        if None or RE.match(self._url) is None:
            self._msg_box.show()
            return

        if not self._go_btn.isEnabled():
            return

        self._table.setRowCount(0)
        self._go_btn.setEnabled(False)

        self._emitter.emit(self._url)

    def all_done(self, *args):
        self._go_btn.setEnabled(True)

    def new_result(self, n: int, row):
        hope_row = Hope(**row)  # type: Hope

        self._table.insertRow(n)
        self._table.setItem(n, 0, QTableWidgetItem(hope_row.url.rstrip('/')))
        self._table.setItem(n, 1, QTableWidgetItem(str(hope_row.status)))
        self._table.setItem(n, 2, QTableWidgetItem("{:0.5f}".format(hope_row.time).rstrip('0')))

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
