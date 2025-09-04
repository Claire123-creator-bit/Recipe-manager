from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///recipes.db")  # or your actual database URL
SessionLocal = sessionmaker(bind=engine)

from app.models import Base

Base.metadata.create_all(bind=engine)
