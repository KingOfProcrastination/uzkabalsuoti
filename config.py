from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import os

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'postgresql',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST': os.environ['RDS_HOSTNAME'],
            'PORT': os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'postgresql',
            'NAME': 'elections_data',
            'USER': '',
            'PASSWORD': os.environ["password"] ,
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
# Fetch database configuration from the DATABASES dictionary
db_config = DATABASES['default']

# Construct the database URL
DB_URL = f"postgresql://{db_config['USER']}:{db_config['PASSWORD']}@{db_config['HOST']}:{db_config['PORT']}/{db_config['NAME']}"
DB_ENGINE = create_engine(DB_URL)
DB_SESSION: Union[Session, scoped_session] = scoped_session(sessionmaker(bind=DB_ENGINE))