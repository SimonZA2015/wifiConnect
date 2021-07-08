import os
import socket
import time

import tools
from threading import Thread
from main import mainWifi


class mainChecker():
    def __init__(self, ssid, passw, gui=False):
        def editGui(text):
            if not (self.gui == False):
                tools.pyqt5.setInfo(self.gui, "🐎checking internet connection..🐎✅internet on✅ ")

        self.ssid = ssid
        self.passw = passw
        self.gui = gui
        print('<checker started>')
        if not (self.gui == False):
            Thread(target= lambda: self.start(editGui)).start()
            tools.pyqt5.setInfo(self.gui, '<checker started>')
        else:
            self.start(editGui)

    def start(self, gui):
        while True:
            result = self.check("www.google.com", gui)
            if not result:
                mainWifi(self.ssid, self.passw)
                time.sleep(3)
            time.sleep(2)

    def check(self, url, gui):
        for timeout in [1, 5]:
            try:
                clear = lambda: os.system('clear')
                clear()
                print("🐎checking internet connection..🐎")
                socket.setdefaulttimeout(timeout)
                host = socket.gethostbyname(url)
                s = socket.create_connection((host, 80), 2)
                s.close()
                print('      ✅internet on✅ ')
                gui("🐎checking internet connection..🐎\n      ✅internet on✅ ")
                return True
            except Exception as e:
                print(e)
                print("      internet off✔")
                if not (self.gui == False):
                    tools.pyqt5.setInfo(self.gui, str(e) + "\n      internet off✔")
                return False


if __name__ == "__main__":
    ssid = 'RT-5GPON-C544'
    passw = 'ZYGSRRAA'
    ssid_t = input('ssid>')
    passw_t = input('pass>')
    if len(ssid_t) > 0 and len(passw_t):
        ssid = ssid_t
        passw = passw_t
    st = mainChecker(ssid, passw)
