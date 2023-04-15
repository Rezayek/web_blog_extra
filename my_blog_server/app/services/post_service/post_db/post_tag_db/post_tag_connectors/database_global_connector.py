from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.db_holder_dic.database import Base
from app.config_env import settings
#SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'


# def global_connector(tag:str):
#     SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_{tag}'

#     engine = create_engine(SQLALCHEMY_DATABASE_URL)

#     sessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)


#     Base.metadata.create_all(bind=engine)


#     db = sessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


class DBConnector:
    
    def __init__(self, tag: str):
        self.tag = tag
        
        
    def __enter__(self):
        self.db = self.db_connector()
        return self.db

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def db_connector(self):
        SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_{self.tag}'
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = sessionLocal()
        return db