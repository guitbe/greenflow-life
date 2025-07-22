from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class DietaryPreference(enum.Enum):
    OMNIVORE = "omnivore"
    VEGETARIAN = "vegetarian"
    VEGAN = "vegan"
    PESCATARIAN = "pescatarian"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    name = Column(String, nullable=False)
    profile_image_url = Column(String, nullable=True)
    birth_date = Column(Date, nullable=True)
    dietary_preference = Column(Enum(DietaryPreference), default=DietaryPreference.OMNIVORE)
    target_carbon_reduction = Column(Float, default=20.0)  # percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    meal_logs = relationship("MealLog", back_populates="user")
    user_challenges = relationship("UserChallenge", back_populates="user")
    user_badges = relationship("UserBadge", back_populates="user")
    activity_logs = relationship("ActivityLog", back_populates="user") 