import sqlalchemy
import os
from sqlalchemy.ext.declarative import declarative_base
from dbmodels import Base, DialogRecord


def create_engine():
    ip = os.environ["ADVSVC_DB_IP"]
    port = os.environ["ADVSVC_DB_PORT"]
    user = os.environ["ADVSVC_DB_USER"]
    passwd = os.environ["ADVSVC_DB_PASSWD"]
    db = os.environ["ADVSVC_DB_DBNAME"]
    url = f"postgresql://{user}:{passwd}@{ip}:{port}/{db}"
    engine = sqlalchemy.create_engine(url, echo=True)

    return engine


def init_db():
    # create engine
    engine = create_engine()
    # initialize tables
    # associate model and engine
    # initialize table
    Base.metadata.create_all(bind=engine)

def drop_all():
    engine = create_engine()
    Base.metadata.drop_all(bind=engine)
