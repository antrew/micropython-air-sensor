import network


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
