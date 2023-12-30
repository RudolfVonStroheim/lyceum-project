from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog, QTableWidgetItem, QAbstractItemView
from table import Table
from PyQt5.uic import loadUi


class ChooseWindow(QDialog):
    station = pyqtSignal(int, list, bool)

    def __init__(self):
        super().__init__()
        loadUi('edit.ui', self)
        self.table = Table('stations.db')
        self.stations = self.table.search()
        self.set_table()
        self.index = 0
        self.stations_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.choose.clicked.connect(self.accept)
        self.search.clicked.connect(self.update_search)
        self.cancel.clicked.connect(self.close)
        self.delete_2.clicked.connect(self.delete)

    def accept(self):
        selected_station = tuple(map(lambda x: x.text(), self.stations_table.selectedItems()))
        data = list(map(lambda x: tuple(x[0:3]), self.stations))
        data = [tuple(map(str, d)) for d in data]
        index = data.index(selected_station)
        stations = self.stations.copy()
        self.station.emit(index, stations, True)
        super().accept()

    def delete(self):
        item = self.stations_table.selectedItems()
        item_id = item[-1].text()
        self.table.delete(item_id)
        self.update_search()
        self.set_table()

    def closeEvent(self, event):
        del self.table
        self.station.emit(0, [], False)
        super().closeEvent(event)

    def update_search(self):
        name, genre = map(lambda x: x.text(), [self.name, self.genre])
        self.stations = self.table.search(name=name, genre=genre)
        self.set_table()

    def set_table(self):
        self.stations_table.setColumnCount(3)
        self.stations_table.setRowCount(0)
        for i, row in enumerate(self.stations):
            self.stations_table.setRowCount(self.stations_table.rowCount() + 1)
            for j, elem in enumerate(row):
                if j != 3:
                    self.stations_table.setItem(i, j, QTableWidgetItem(str(elem)))