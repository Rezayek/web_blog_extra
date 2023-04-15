import firebase_admin
from firebase_admin import credentials, firestore
from app.config_env import settings
from fastapi import status, HTTPException

def singleton(class_instance):
    instances = {}
    def get_instance(*args, **kwargs):
        if class_instance not in instances:
            instances[class_instance] = class_instance(*args, **kwargs)
        return instances[class_instance]
    return get_instance

@singleton
class FirebaseConnector:
    
    
    def firebase_connector(self):
        try:
            cred = credentials.Certificate(f"{settings.cred_file}")
            firebase_admin.initialize_app(cred)
            return firestore.client()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Service is down for now please wait")
        
firebase_db = FirebaseConnector().firebase_connector()

    