from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class MealType(enum.Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

class MealLog(Base):
    __tablename__ = "meal_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food_name = Column(String, nullable=False)
    portion_size = Column(Float, nullable=False)  # in grams
    meal_type = Column(Enum(MealType), nullable=False)
    carbon_footprint = Column(Float, nullable=False)  # kg CO2e
    image_url = Column(String, nullable=True)
    logged_at = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="meal_logs")
    recommended_swaps = relationship("RecommendedSwap", back_populates="meal_log") 