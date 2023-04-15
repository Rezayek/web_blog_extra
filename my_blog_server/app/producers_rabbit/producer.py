import pika
import os
import sys
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../..'))
sys.path.append(parent_dir)

from app.config_env import settings

def producer_post(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.producer_host_post))
    channel = connection.channel()

    channel.queue_declare(queue=settings.producer_queue_post)

    channel.basic_publish(exchange='', routing_key=settings.producer_routing_key_post, body=f'{body}')
    print(" [x] Sent msg sended'")
    connection.close()
        
def producer_user(body):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.producer_host_user))
    channel = connection.channel()

    channel.queue_declare(queue=settings.producer_queue_user)

    channel.basic_publish(exchange='', routing_key=settings.producer_routing_key_user, body=f'{body}')
    print(" [x] Sent msg sended'")
    connection.close()
    
def producer_user_sub(body):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=settings.producer_host_user_sub))
    channel = connection.channel()

    channel.queue_declare(queue=settings.producer_queue_user_sub)

    channel.basic_publish(exchange='', routing_key=settings.producer_routing_key_user_sub, body=f'{body}')
    print(" [x] Sent msg sended'")
    connection.close()