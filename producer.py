import json
import time
import random
import logging
from kafka import KafkaProducer
from kafka.errors import KafkaError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)

# Simulate user activity data
users = ['user1', 'user2', 'user3', 'user4']
events = ['click', 'view', 'purchase']

try:
    while True:
        message = {
            "user_id": random.choice(users),
            "event": random.choice(events),
            "timestamp": int(time.time())
        }
        key = message['user_id']
        try:
            producer.send('user-activity', key=key, value=message).get(timeout=10)
            logger.info(f"Sent: {message}")
        except KafkaError as e:
            logger.error(f"Failed to send message: {e}")
        time.sleep(1)  # Simulate a delay
except KeyboardInterrupt:
    logger.info("Stopping producer...")
finally:
    producer.close()
