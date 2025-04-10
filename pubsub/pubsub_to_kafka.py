import json
import os
from google.cloud import pubsub_v1
from kafka import KafkaProducer

# Set GCP credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\yslog\PycharmProjects\PythonProject\secrets\csye7125-dev-449823-864c66dd2feb.json"

# GCP Pub/Sub setup
project_id = "csye7125-dev-449823"
subscription_id = "gcs-subscription"
subscription_path = f"projects/{project_id}/subscriptions/{subscription_id}"

# Kafka setup
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)
kafka_topic = "gcs-topic"

def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    if 'name' in data and data.get("contentType", "") == "application/pdf":
        payload = {
            "bucket": data.get("bucket", ""),
            "file": data.get("name", ""),
            "eventType": data.get("eventType", "OBJECT_FINALIZE"),
            "source": "pubsub-trigger",
            "triggered_by": "gcs-upload"
        }
        producer.send(kafka_topic, value=payload)
        print(f"✅ Sent to Kafka: {payload}")
    else:
        print(f"⚠️ Skipped non-PDF or invalid event: {data}")
    message.ack()

if __name__ == "__main__":
    subscriber = pubsub_v1.SubscriberClient()
    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"🔁 Listening for GCS → Pub/Sub events on: {subscription_path}")
    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        print("👋 Exiting...")
        streaming_pull_future.cancel()
