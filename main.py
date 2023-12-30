from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.uic import loadUi
from sys import argv, exit
from add import AddWindow
from choose import ChooseWindow
from json import load
from settings import SettingsWindow
import socks
import socket


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ip = None
        self.index = None
        self.port = None
        self.save_dir = None
        self.update_settings()
        loadUi('main.ui', self)
        self.player = QMediaPlayer()
        self.stations = []
        self.volume = 50
        self.update_volume()
        self.player.setVolume(self.volume)
        self.choose()
        self.add_station.clicked.connect(self.add)
        self.sync_btn.clicked.connect(self.sync)
        self.change_station.clicked.connect(self.choose)
        self.volume_slider.valueChanged[int].connect(self.change_volume)
        self.play_btn.clicked.connect(self.play)
        self.switch_left_btn.clicked.connect(self.switch_left)
        self.settings_btn.clicked.connect(self.change_settings)
        self.record_btn.clicked.connect(self.start_record)
        self.switch_right_btn.clicked.connect(self.switch_right)
        self.player.error.connect(self.handle_error)

    def change_settings(self):
        settings = SettingsWindow()
        settings.exec_()
        self.update_settings()

    def start_record(self):
        pass

    def sync(self):
        self.player.stop()
        self.set()

    def update_settings(self):
        with open('settings.json', 'r') as sett_file:
            settings = load(sett_file)
        self.ip = settings['ip']
        self.port = settings['port']
        self.save_dir = settings['dir']
        self.init_proxy()

    def handle_error(self, error):
        msg = QMessageBox()
        msg.setIcon(msg.critical)
        msg.setText(error)
        msg.exec_()
        self.close()

    def change_volume(self, volume):
        self.volume = volume
        self.player.setVolume(volume)

    def add(self):
        a = AddWindow()
        a.exec_()

    def choose(self):
        choose_window = ChooseWindow()
        choose_window.station.connect(self.handle)
        choose_window.exec_()

    def play(self):
        self.player.play()
        self.play_btn.clicked.connect(self.pause)
        self.play_btn.setText('||')

    def pause(self):
        self.player.pause()
        self.play_btn.clicked.connect(self.play)
        self.play_btn.setText('►')

    def handle(self, index, stations, flag):
        if flag:
            self.index = index
            self.stations = stations
            self.set()

    def set(self):
        self.statusBar().showMessage(self.stations[self.index][0])
        media_content = QMediaContent(QUrl(self.stations[self.index][-1]))
        if media_content.isNull():
            print("Ошибка: Не удалось установить медиаконтент")
        else:
            self.player.setMedia(media_content)
            self.play()
        self.play()

    def switch_left(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.stations) - 1
        self.set()

    def switch_right(self):
        self.index += 1
        if self.index >= len(self.stations):
            self.index = 0
        self.set()


if __name__ == '__main__':
    app = QApplication(argv)
    main = Main()
    main.show()
    exit(app.exec_())
