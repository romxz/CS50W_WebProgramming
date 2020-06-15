import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

def getDatabase():
    # Set up database
    engine = create_engine(os.getenv("DATABASE_URL"))
    return scoped_session(sessionmaker(bind=engine))