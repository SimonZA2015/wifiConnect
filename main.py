import os

import dbus
import time

class mainWifi():
    def __init__(self, ssid, passw):
        self.bus = dbus.SystemBus()
        self.manager_bus_object = self.bus.get_object("org.freedesktop.NetworkManager",
                                            "/org/freedesktop/NetworkManager")
        self.manager = dbus.Interface(self.manager_bus_object,
                                 "org.freedesktop.NetworkManager")
        self.manager_props = dbus.Interface(self.manager_bus_object,
                                       "org.freedesktop.DBus.Properties")
        self.was_wifi_enabled = self.manager_props.Get("org.freedesktop.NetworkManager",
                                             "WirelessEnabled")
        self.checkEnabledWifi()
        self.setWifiMonitor()
        self.getListsSsids(ssid)
        self.connectingWifi(passw)

        
    def checkEnabledWifi(self):
        if not self.was_wifi_enabled:
            self.manager_props.Set("org.freedesktop.NetworkManager", "WirelessEnabled",
                              True)

    def setWifiMonitor(self):
        self.device_path = self.manager.GetDeviceByIpIface("wlan0")
        self.device = dbus.Interface(self.bus.get_object("org.freedesktop.NetworkManager",
                                               self.device_path),
                                "org.freedesktop.NetworkManager.Device.Wireless")
        self.accesspoints_paths_list = self.device.GetAccessPoints()

    def getListsSsids(self, ssid):
        self.our_ap_path = None
        for ap_path in self.accesspoints_paths_list:
            ap_props = dbus.Interface(
                self.bus.get_object("org.freedesktop.NetworkManager", ap_path),
                "org.freedesktop.DBus.Properties")
            ap_ssid = ap_props.Get("org.freedesktop.NetworkManager.AccessPoint",
                                   "Ssid")
            # Returned SSID is a list of ASCII values. Let's convert it to a proper
            # string.
            str_ap_ssid = "".join(chr(i) for i in ap_ssid)
            print(str_ap_ssid)
            if str_ap_ssid == ssid:
                self.our_ap_path = ap_path
                print('connecting to: ' + str_ap_ssid)
                break
        if not self.our_ap_path:
            self.print("AP not found :(")
            exit(2)

    def connectingWifi(self, passw):
        NM_ACTIVE_CONNECTION_STATE_ACTIVATED = 2
        state = 0
        connection_params = {
            "802-11-wireless": {
                "security": "802-11-wireless-security",
            },
            "802-11-wireless-security": {
                "key-mgmt": "wpa-psk",
                "psk": passw
            },
        }
        settings_path, connection_path = self.manager.AddAndActivateConnection(
            connection_params, self.device_path, self.our_ap_path)
        connection_props = dbus.Interface(
            self.bus.get_object("org.freedesktop.NetworkManager", connection_path),
            "org.freedesktop.DBus.Properties")
        while True:
            try:
                state = connection_props.Get(
                    "org.freedesktop.NetworkManager.Connection.Active", "State")
                if state == NM_ACTIVE_CONNECTION_STATE_ACTIVATED:
                    break
                time.sleep(0.001)
            except:
                print('ERROR main.py: incorrect password')
                break

        self.print("Connection established!")

    def print(self, text):
        os.system('clear')
        print(text)

if __name__ == "__main__":
    st = mainWifi()