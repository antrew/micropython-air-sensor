import urequests
from config import LOGSTASH_URL


def send_data_to_logstash(url, data):
    print('Sending data to Logstash. URL:', url, 'Data:', data)
    try:
        response = urequests.post(
            url,
            json=data
        )
        print(response.status_code, response.reason, response.text)
    except OSError as e:
        print('Error sending data to Logstash:', e)


send_data_to_logstash(LOGSTASH_URL, {
    'device_id': 'test',
    'temperature': 999,
    'humidity': 99,
})
