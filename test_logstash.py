from config import LOGSTASH_URL
from logstash import send_data_to_logstash

send_data_to_logstash(LOGSTASH_URL, {
    'device_id': 'test',
    'temperature': 999,
    'humidity': 99,
})
