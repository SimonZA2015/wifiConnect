import sys
from PyQt5.QtWidgets import QApplication, QLabel, QCheckBox, QHBoxLayout, QVBoxLayout, QLineEdit, QMainWindow, QFrame, \
    QPushButton, QSpinBox

import tools
from checkerNetwork import mainChecker
from main import mainWifi
import pygame


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🐎WifiReconnect🐎")
        pygame.init()
        self.setFixedWidth(pygame.display.Info().current_w//3)
        self.setFixedHeight(pygame.display.Info().current_h//3)
        self.home()

    def home(self):
        hframe = QFrame()
        vframe = QFrame()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        label = QLabel('Ведите данные сети')
        label2 = QLabel('🐎WifiReconnect🐎')
        self.wifiList = tools.wifi.getList(self)
        self.inputSsid = QSpinBox(value=0, maximum=len(self.wifiList) - 1, minimum=0, suffix=self.wifiList[0])
        self.inputPass = QLineEdit()
        # self.inputSsid.setPlaceholderText('Название сети')
        self.inputSsid.valueChanged.connect(self.onChangedValue)
        self.inputPass.setPlaceholderText('Пароль от сети')
        go = QPushButton('Подключиться')
        self.check = QCheckBox('С проверкой на интернет')

        go.clicked.connect(self.goto)

        vbox.addWidget(label)
        vbox.addWidget(self.inputSsid)
        vbox.addWidget(self.inputPass)
        vbox.addWidget(go)
        vbox.addWidget(self.check)

        vframe.setLayout(vbox)

        hbox.addWidget(label2)
        hbox.addWidget(vframe)

        hframe.setLayout(hbox)

        self.setCentralWidget(hframe)

    def onChangedValue(self, i):
        self.inputSsid.setSuffix(self.wifiList[i])

    def goto(self):
        ssid = self.wifiList[int(self.inputSsid.value())]
        print('selected: ' + ssid)
        print(self.check.isChecked())
        if self.check.isChecked():
            mainChecker(ssid, self.inputPass.text(), gui=self)
        else:
            mainWifi(ssid, self.inputPass.text())


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
