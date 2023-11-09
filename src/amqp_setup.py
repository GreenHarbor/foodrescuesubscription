import time
from os import environ
import pika
from logger import logger

if environ.get("stage") == "dev" or environ.get("stage") == "test":
    HOSTNAME = environ.get('rabbitmq_host')
    PORT = environ.get('rabbitmq_port')
else:
    HOSTNAME = "AWS_URL"
    PORT = "AWS_PORT"

# Create a connection and channel
retry_timer = 2
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=HOSTNAME,
                port=PORT,
                virtual_host='/'))
        logger.info("Connected to Rabbit MQ SUCCESS!")
        break
    except Exception:
        logger.info(f"Connecting to RabbitMQ Failed... Retrying in {retry_timer} seconds")
        time.sleep(retry_timer)
        retry_timer += 2

channel = connection.channel()

# Create an AMQP topic exchange for Notifications
exchange_name = "greenharbor.topic"
exchange_type = "topic"
channel.exchange_declare(
    exchange=exchange_name,
    exchange_type=exchange_type,
    durable=True
)

# Declare queues
consume_queue_name = 'Foodrescue_New_Post'
channel.queue_declare(
    queue=consume_queue_name,
    durable=True
)

publish_queue_name = 'Foodrescue_Notification'
channel.queue_declare(
    queue=publish_queue_name,
    durable=True
)

# Bind queues
consume_routing_key = 'foodrescue_post.*'
channel.queue_bind(
    exchange=exchange_name,
    queue=consume_queue_name,
    routing_key=consume_routing_key
)

publish_routing_key = 'foodrescue_notification.*'
channel.queue_bind(
    exchange=exchange_name,
    queue=publish_queue_name,
    routing_key=publish_routing_key
)
