from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

# Define the database URI and create an engine
DATABASE_URI = 'sqlite:///inventory.db'
engine = create_engine(DATABASE_URI)

# Create a session
Session = sessionmaker(bind=engine)


def init_db():
    # Create all tables in the database
    Base.metadata.create_all(engine)


