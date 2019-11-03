import network
import utime


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
    print('Connecting to WLAN {}'.format(ssid))
    sta_if.connect(ssid, password)
    counter = 0
    while not sta_if.isconnected():
        if counter > 20:
            raise TimeoutError("Timeout connecting to WLAN")
        counter += 1
        print('Waiting for WLAN connection...')
        utime.sleep(1)
    print('Connected')
    print('network config:', sta_if.ifconfig())


def disable_access_point():
    network.WLAN(network.AP_IF).active(False)
