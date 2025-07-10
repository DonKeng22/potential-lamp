"""
Script to create all tables in the database using SQLAlchemy models.
"""
from data.models import Base
from data.db import engine

if __name__ == "__main__":
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    print("Done.")
