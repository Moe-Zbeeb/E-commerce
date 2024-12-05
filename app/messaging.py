# File: /home/mohammad/E-commerce-1/app/messaging.py
import pika
import time  # Import time module
from app.extensions import logger  # Import the logger
import os  # Import os module

# Connection parameters for RabbitMQ
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
QUEUE_NAME = 'sales_notifications'

def setup_channel():
    """Establish connection and return a channel."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)  # Ensure the queue exists
    return channel, connection

def publish_message(message):
    """Publish a message to the queue."""
    channel, connection = setup_channel()
    channel.basic_publish(exchange='', routing_key=QUEUE_NAME, body=message)
    logger.info(f"[x] Sent: {message}")
    connection.close()

def consume_messages(callback):
    """Consume messages from the queue."""
    channel, connection = setup_channel()

    def on_message(ch, method, properties, body):
        start_time = time.time()
        logger.info(f"[x] Received: {body.decode()}")
        callback(body.decode())
        elapsed_time = time.time() - start_time
        logger.info(f"Message processed in {elapsed_time:.4f}s")

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message, auto_ack=True)
    logger.info("[*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()
