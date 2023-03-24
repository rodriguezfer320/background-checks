from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

engine = create_engine('postgresql://{user}:{password}@{host}:{port}/{database}'.format(
    user=config('PGSQL_USER'),
    password=config('PGSQL_PASSWORD'),
    host=config('PGSQL_HOST'),
    port=config('PGSQL_PORT'),
    database=config('PGSQL_DATABASE')
))

Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()