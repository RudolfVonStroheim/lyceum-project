from PyQt5.QtWidgets import QDialog, QFileDialog
from json import dump, load
from PyQt5.uic import loadUi
from os import getcwd

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.cwd = getcwd()
        loadUi('settings.ui', self)
        self.load_data()
        self.ok_btn.clicked.connect(self.submit)
        self.cancel_btn.clicked.connect(self.close)
        self.change_path_btn.clicked.connect(self.change_dir)

    def change_dir(self):
        pass

    def submit(self):
        self.settings['ip'] = self.ip_line.text
        self.settings['port'] = self.port_line.text()
        self.settings['dir'] = self.path_lbl.text.rstrip('cwd:/')
        with open('settings.json', 'w') as settings_file:
            dump(self.settings, settings_file)
        self.close()

    def load_data(self):
        with open('settings.json', 'r') as settings_file:
            self.settings = load(settings_file)
        self.path_lbl.setText('cwd:/' + self.settings['dir'])
        self.ip_line.setText(self.settings['ip'])
        self.port_line.setText(self.settings['port'])