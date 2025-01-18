import json
import os
from configparser import ConfigParser
from datetime import datetime
import time

import yaml
from kafka import KafkaProducer
import yfinance  as yf

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yml")
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

kafka_host_name = config['kafka'].get('host')
kafka_port_no = config['kafka'].get('port_no')
KAFKA_TOPIC_NAME_CONS = config['kafka'].get('input_topic_name')
KAFKA_BOOTSTRAP_SERVERS_CONS = kafka_host_name + ':' + kafka_port_no
# return data
if __name__ == "__main__":
    df = yf.download(
        tickers=['KLS.AX'],
        period='max',
        interval='1m',
        threads=True,
        group_by='ticker')
    df.reset_index(inplace=True)
    json_data = df.to_json(orient='records')

    kafka_producer_obj = KafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
                                       value_serializer=lambda x: json.dumps(x).encode('utf-8'))
    for data in json.loads(json_data):
        data['Symbol']='KLS.AX'
        print("Message: ", data)
        kafka_producer_obj.send(KAFKA_TOPIC_NAME_CONS, data)
        time.sleep(1)

