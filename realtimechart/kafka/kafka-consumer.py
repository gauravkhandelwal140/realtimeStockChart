import asyncio
import os
import yaml
from kafka import KafkaConsumer

KAFKA_CONSUMER_GROUP_NAME_CONS = "test-consumer-group"
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.yml")
with open(CONFIG_PATH, "r") as file:
    config = yaml.safe_load(file)

kafka_host_name = config['kafka'].get('host')
kafka_port_no = config['kafka'].get('port_no')
KAFKA_TOPIC_NAME_CONS = config['kafka'].get('input_topic_name')
KAFKA_BOOTSTRAP_SERVERS_CONS = kafka_host_name + ':' + kafka_port_no

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realtimechart.realtimechart.settings')
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

async def send_to_websocket(message):
    # Send the Kafka message to the specific WebSocket (using the user/channel name)
    await channel_layer.group_send(
        'ws_stock',  # The WebSocket consumer channel name (this could be user-specific)
        {
            'type': 'send_stock_data',  # The event type
            'message': message
        }
    )


if __name__ == "__main__":
    print("Kafka Consumer Application Started ... ")
    try:
        consumer = KafkaConsumer(
        KAFKA_TOPIC_NAME_CONS,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id=KAFKA_CONSUMER_GROUP_NAME_CONS,
        value_deserializer=lambda x: x.decode('utf-8'))
        for message in consumer:
            message = message.value
            asyncio.run(send_to_websocket(message))
            print("Message received: ", message)
        # asyncio.run(send_to_websocket('Hello'))

    except Exception as ex:
        print("Failed to read kafka message.")
        print(ex)