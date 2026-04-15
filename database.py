from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup (SQLite - simple aur local ke liye best)
engine = create_engine("sqlite:///app.db", echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Lead table (hum isme leads store karenge)
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    status = Column(String, default="new")
    transcript = Column(Text, default="")

# Pehli baar table create kar do
Base.metadata.create_all(bind=engine)