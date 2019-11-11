import urequests
from config import LOGSTASH_URL


class Logstash:
    def __init__(self):
        self.url = LOGSTASH_URL
        print('Logstash URL: ', self.url)

    def send_data(self, data):
        print('Sending data to Logstash. URL:', self.url, 'Data:', data)
        try:
            response = urequests.post(
                self.url,
                json=data
            )
            print(response.status_code, response.reason, response.text)
        except OSError as e:
            print('Error sending data to Logstash:', e)
