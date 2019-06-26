import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# These env variables are the same ones used for the DB container
engine = create_engine(os.environ['DATABASE_URL']) 

Base = declarative_base()

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import models
    from models import Users
    Base.metadata.create_all(bind=engine)

