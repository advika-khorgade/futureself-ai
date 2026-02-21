"""Database models and initialization."""
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

Base = declarative_base()


class User(Base):
    """User model."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)


class DecisionHistory(Base):
    """Decision history model."""
    __tablename__ = "decision_history"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    decision_text = Column(Text, nullable=False)
    context = Column(Text)
    timeframe = Column(String(100))
    recommendation = Column(String(100))
    confidence_level = Column(Float)
    risk_score = Column(Float)
    opportunity_score = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    full_analysis = Column(Text)  # JSON string of full analysis


def init_db():
    """Initialize the database."""
    # Create data directory if it doesn't exist
    os.makedirs("data", exist_ok=True)
    
    # Create database
    engine = create_engine("sqlite:///data/futureself.db")
    Base.metadata.create_all(engine)
    
    return engine


def get_session():
    """Get database session."""
    engine = create_engine("sqlite:///data/futureself.db")
    Session = sessionmaker(bind=engine)
    return Session()
