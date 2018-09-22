import network
from config import WLAN_SSID, WLAN_PASSWORD
from wlan import do_connect, print_status

print_status('Station', network.WLAN(network.STA_IF))
print_status('Access Point', network.WLAN(network.AP_IF))

do_connect(WLAN_SSID, WLAN_PASSWORD)
