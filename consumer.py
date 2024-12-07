import json
import psycopg2
from confluent_kafka import Consumer, KafkaError

# Kafka Consumer Configuration
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'activity-group',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True
}
consumer = Consumer(consumer_config)

# Subscribe to the Kafka topic
consumer.subscribe(['user-activity'])

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='kafka_db',
    user='kafka_user',
    password='kafka_password',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Create a table for user activity
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_activity (
        user_id TEXT,
        event TEXT,
        timestamp BIGINT
    )
''')
conn.commit()

print("Starting consumer...")
try:
    while True:
        msg = consumer.poll(timeout=1.0)  # Poll for messages with a 1-second timeout

        if msg is None:
            continue  # No new messages
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"End of partition reached: {msg.topic()} [{msg.partition()}]")
                continue
            else:
                print(f"Consumer error: {msg.error()}")
                break

        # Deserialize the message
        record = json.loads(msg.value().decode('utf-8'))

        # Insert the record into PostgreSQL
        cursor.execute('''
            INSERT INTO user_activity (user_id, event, timestamp)
            VALUES (%s, %s, %s)
        ''', (record['user_id'], record['event'], record['timestamp']))
        conn.commit()

        print(f"Processed: {record}")

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    # Close resources
    consumer.close()
    cursor.close()
    conn.close()
