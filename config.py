from typing import Union
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session
import os

if 'RENDER_DB_NAME' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE': 'postgresql',
            'NAME': os.environ['RENDER_DB_NAME'],
            'USER': os.environ['RENDER_USERNAME'],
            'PASSWORD': os.environ['RENDER_PASSWORD'],
            'HOST': os.environ['RENDER_HOSTNAME'],
            'PORT': os.environ['RENDER_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'postgresql',
            'NAME': 'elections_data',
            'USER': 'postgres',
            'PASSWORD': os.environ["DB_password"] ,
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