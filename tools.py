import dbus
from PyQt5.QtWidgets import QLabel, QPushButton, QFrame, QHBoxLayout, QVBoxLayout


class pyqt5():
    def __init__(self):
        p = 0

    def setInfo(self, text):
        print('setOnfo: >' + text, self)
        label = QLabel(text)
        buttonCansel = QPushButton('cansel')
        hframe = QFrame()
        vframe = QFrame()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        label2 = QLabel('🐎WifiReconnect🐎')

        vbox.addWidget(label)
        vbox.addWidget(buttonCansel)
        vframe.setLayout(vbox)

        hbox.addWidget(label2)
        hbox.addWidget(vframe)
        hframe.setLayout(hbox)

        self.setCentralWidget(hframe)


class wifi:
    def __init__(self):
        p = 0

    def getList(self):

        list = []
        if system.compatibility(self):
            bus = dbus.SystemBus()
            manager_bus_object = bus.get_object("org.freedesktop.NetworkManager",
                                                "/org/freedesktop/NetworkManager")
            manager = dbus.Interface(manager_bus_object,
                                     "org.freedesktop.NetworkManager")
            device_path = manager.GetDeviceByIpIface("wlan0")
            device = dbus.Interface(bus.get_object("org.freedesktop.NetworkManager",
                                                   device_path),
                                    "org.freedesktop.NetworkManager.Device.Wireless")
            accesspoints_paths_list = device.GetAccessPoints()
            for ap_path in accesspoints_paths_list:
                ap_props = dbus.Interface(
                    bus.get_object("org.freedesktop.NetworkManager", ap_path),
                    "org.freedesktop.DBus.Properties")
                ap_ssid = ap_props.Get("org.freedesktop.NetworkManager.AccessPoint",
                                       "Ssid")
                # Returned SSID is a list of ASCII values. Let's convert it to a proper
                # string.
                str_ap_ssid = "".join(chr(i) for i in ap_ssid)
                print(str_ap_ssid)
                list.append(str_ap_ssid)
        else:
            list.append('Не поддерживаемая система')

        return list

class system():
    def compatibility(self):
        import platform
        if platform.system() == 'Linux':
            return True
        else:
            return False
