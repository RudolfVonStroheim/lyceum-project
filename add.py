from PyQt5.QtWidgets import QDialog
from PyQt5.uic import loadUi
from table import Table


class AddWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('add.ui', self)
        self.table = Table('stations.db')
        self.cancel.clicked.connect(self.close)
        self.add.clicked.connect(self.add_func)

    def add_func(self):
        name, link, genre = self.name.text(), self.link.text(), self.genre.text()
        self.table.add(name, link, genre)
        self.close()

    def closeEvent(self, event):
        del self.table
        super().closeEvent(event)
