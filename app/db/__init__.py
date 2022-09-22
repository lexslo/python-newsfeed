from os import getenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
# global variable
from flask import g

load_dotenv()

# connect to database using env

# manages the overall connection to the database.
engine = create_engine(getenv('DB_URL'), echo=True, pool_size=20, max_overflow=0)
# generates temporary connections for performing create, read, update, and delete (CRUD) operations.
Session = sessionmaker(bind=engine)
# helps us map the models to real MySQL tables.
Base = declarative_base()

def init_db(app):
    Base.metadata.create_all(engine)

    app.teardown_appcontext(close_db)

# returns a new session-connection object whenever this function is called
def get_db():
    # saves the current connection on the g object, if it's not already there
    if  'db' not in g:
        # store connection in app context
        print('Inside get_db()')
        g.db = Session()
    # returns the connection from the g object instead of creating a new Session instance each time
    return g.db

def close_db(e=None):
    # attempts to find and remove db from the g object
    db = g.pop('db', None)
    # If db exists (that is, db doesn't equal None), then db.close() will end the connection
    if db is not None:
        db.close()
