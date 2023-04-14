import pika
import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../..'))
sys.path.append(parent_dir)

from app.config_env import settings

def producer(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.producer_host))
    channel = connection.channel()

    channel.queue_declare(queue=settings.producer_queue)

    channel.basic_publish(exchange='', routing_key=settings.producer_routing_key, body=f'{body}')
    print(" [x] Sent msg sended'")
    connection.close()