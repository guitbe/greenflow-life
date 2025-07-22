from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class RecommendedSwap(Base):
    __tablename__ = "recommended_swaps"
    
    id = Column(Integer, primary_key=True, index=True)
    meal_log_id = Column(Integer, ForeignKey("meal_logs.id"), nullable=False)
    original_food = Column(String, nullable=False)
    recommended_food = Column(String, nullable=False)
    carbon_reduction = Column(Float, nullable=False)  # kg CO2e saved
    recommendation_message = Column(Text, nullable=False)
    accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    meal_log = relationship("MealLog", back_populates="recommended_swaps") 