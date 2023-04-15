import pika
import json
from datetime import datetime
import os
import sys
import ast
# Get the path of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Add the path of the parent directory to the system path
parent_dir = os.path.abspath(os.path.join(current_dir, '../../../../../..'))
sys.path.append(parent_dir)

# Now you can import settings from util.config
from app.config_env import settings
from app.services.post_service.post_db.post_tag_db.post_db_tag_provider import PostDbTagProvider 
from app.app_models.db_models import User
from app.debugger_file import set_up_logger

post_db_tag_provider = PostDbTagProvider()
user_log = set_up_logger(file_name= settings.log_user_listener) 


def launch_user_Listenner():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=settings.producer_host_user_sub))
    channel = connection.channel()

    channel.queue_declare(queue=settings.producer_queue_user_sub)
    
    # Set prefetch_count to 1
    channel.basic_qos(prefetch_count=1)
    
    def callback(ch, method, properties, body):
        # ch.basic_ack(delivery_tag=method.delivery_tag)
        try:

            # Convert byte string to string
            str_data = body.decode('utf-8')

            # Use ast.literal_eval to safely evaluate the string into a dictionary
            data_dict = ast.literal_eval(str_data) 
            
            user_data = User(**data_dict)
            
            success = post_db_tag_provider.add_new_user(user_data = user_data)
            
            
            
            if success:
                ch.basic_ack(delivery_tag=method.delivery_tag)
                
        except Exception as e:
            user_log.debug(f"Failed to add user to sub databases error : {e} || body : {body}")
            

    channel.basic_consume(queue=settings.producer_queue_user_sub, on_message_callback=callback, auto_ack=False)

    print(' [*] user listener:  Waiting for messages.')
    channel.start_consuming()

def run_user_listener():
    
    try:
        # print("Novel listenner is running. Press Ctrl+Shift+n to stop.")
        # keyboard.add_hotkey('ctrl+shift+s', launch_novel_Listenner)
        launch_user_Listenner()
    except Exception as e :
        print(e)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

if __name__ == "__main__":
    run_user_listener()