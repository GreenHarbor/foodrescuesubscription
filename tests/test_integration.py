import json
import pytest
from src import amqp_setup, logger
import pika

def callback(ch, method, properties, body):
    message_body = json.loads(body)
    assert isinstance(message_body,list)

@pytest.mark.dependency()
def test_get_all():
    logger.logger.info("Starting test")
    amqp_setup.channel.basic_publish(
        exchange=amqp_setup.exchange_name,
        routing_key=amqp_setup.consume_routing_key,
        body=json.dumps({"foodtype": "organic"}),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    
    amqp_setup.channel.basic_consume(
        queue=amqp_setup.publish_queue_name,
        on_message_callback=callback,
        auto_ack=True
    )
