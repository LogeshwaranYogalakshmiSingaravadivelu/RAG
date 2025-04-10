import json
import os
from concurrent.futures import TimeoutError
from google.cloud import pubsub_v1
from kafka import KafkaProducer

# Configure Pub/Sub
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\yslog\PycharmProjects\PythonProject\secrets\csye7125-dev-449823-864c66dd2feb.json"
project_id = "csye7125-dev-449823"
subscription_id = "gcs-subscription"
timeout = 5.0

# Configure Kafka
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
kafka_topic = "gcs-topic"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)


def callback(message):
    print(f"Received message: {message}")
    data = json.loads(message.data.decode("utf-8"))
    # Process the GCS notification data
    if 'name' in data:
        file_info = {
            'bucket': data.get('bucket', ''),
            'name': data.get('name', ''),
            'contentType': data.get('contentType', ''),
            'size': data.get('size', ''),
            'updated': data.get('updated', '')
        }
        # Send to Kafka
        producer.send(kafka_topic, file_info)
        print(f"Sent to Kafka: {file_info}")
    message.ack()


streaming_pull_future = subscriber.subscribe(
    subscription_path, callback=callback
)
print(f"Listening for messages on {subscription_path}")

try:
    streaming_pull_future.result()
except TimeoutError:
    streaming_pull_future.cancel()
    streaming_pull_future.result()