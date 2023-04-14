from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str  
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    mail_password: str
    mail: str
    log_microservice: str
    log_fire_user: str
    log_fire_post: str
    log_fire_comment: str
    log_post_producer: str
    log_user_producer: str
    cred_file: str
    api_gateway_service_host: str
    api_gateway_service_port: int
    auth_service_path: str
    auth_service_host: str
    auth_service_port: int
    posts_service_path: str
    posts_service_host: str
    posts_service_port: int 
    comments_service_path: str
    comments_service_host: str
    comments_service_port: int
    producer_host: str
    producer_queue: str
    producer_routing_key: str


    
    class Config:
        env_file = "./.env"

    
settings = Settings()   
