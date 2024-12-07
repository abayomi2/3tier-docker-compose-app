import json
import time
import random
from confluent_kafka import Producer

# Kafka Configuration
producer_config = {
    'bootstrap.servers': 'localhost:9092'
}
producer = Producer(producer_config)

# Simulate user activity data
users = ['user1', 'user2', 'user3', 'user4']
events = ['click', 'view', 'purchase']

def delivery_report(err, msg):
    if err:
        print(f"Delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

try:
    while True:
        message = {
            "user_id": random.choice(users),
            "event": random.choice(events),
            "timestamp": int(time.time())
        }
        producer.produce('user-activity', key=message['user_id'], value=json.dumps(message), callback=delivery_report)
        producer.flush()  # Ensure messages are sent
        time.sleep(1)  # Simulate delay
except KeyboardInterrupt:
    print("Stopping producer...")
