import json
from datetime import datetime

import pika
import requests

import amqp_setup
from logger import logger

URL = ''


def is_urgent(post):
    current_date = datetime.now().strftime('%Y-%m-%d')
    dateto_date = post.get('dateto').split()[0]
    return dateto_date == current_date


def publish_message(data: str) -> None:
    # Publish to publish queue
    amqp_setup.channel.basic_publish(
        exchange=amqp_setup.exchange_name,
        routing_key=amqp_setup.publish_routing_key,
        body=json.dumps(data),
        properties=pika.BasicProperties(delivery_mode=2)
    )


# What tags? Urgent, distance, organic, vegan
def callback(ch, method, properties, body):
    try:
        # Get message body from queue (what is this for ah?)
        # Even in the original logic, I don't see how message body is used
        message_body = json.loads(body)
        logger.info(message_body)
        # Send a GET request to Cognito
        response = requests.get(URL)
        # If request is not successful, respond and exit
        if response.status_code != 200:
            return
        # If request is successful, get a list of emails
        emails = []
        user_data = response.json()
        user_data = user_data.get('data')
        urgent = message_body.get('foodtype') == 'Urgent'
        vegan = message_body.get('foodtype') == 'Vegan'
        vegetarian = message_body.get('foodtype') == 'Vegetarian'
        organic = message_body.get('foodtype') == 'Organic'
        for user in user_data:
            tags = user.get('tag')
            if urgent and 'urgent' in tags:
                emails.append(user.get('email'))
            if vegan and 'vegan' in tags:
                emails.append(user.get('email'))
            elif vegetarian and 'vegetarian' in tags:
                emails.append(user.get('email'))
            elif organic and 'organic' in tags:
                emails.append(user.get('email'))
        rsp = str({'emails': emails})
        logger.info(f"EMAILS: {emails}")
        publish_message(rsp)
        # Display waiting for message again
        logger.info("Waiting for messages... To exit, press CTRL+C")
    except Exception as e:
        logger.info(e)


if __name__ == '__main__':
    amqp_setup.channel.basic_consume(
        queue=amqp_setup.consume_queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    logger.info("Waiting for messages... To exit, press CTRL+C")
    amqp_setup.channel.start_consuming()
