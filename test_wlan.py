import network
from config import WLAN_SSID, WLAN_PASSWORD


def print_status(wlan_if_name, wlan_if):
    print(
        wlan_if_name, 'status:',
        'active:', wlan_if.active(),
        'connected:', wlan_if.isconnected(),
        'config:', wlan_if.ifconfig()
    )


def do_connect(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)


print_status('Station', network.WLAN(network.STA_IF))
print_status('Access Point', network.WLAN(network.AP_IF))

do_connect(WLAN_SSID, WLAN_PASSWORD)
