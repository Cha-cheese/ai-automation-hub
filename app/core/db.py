from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class UserMemory(Base):
    __tablename__ = "memory"

    user_id = Column(String, primary_key=True)
    data = Column(Text)


def init_db():
    Base.metadata.create_all(bind=engine)