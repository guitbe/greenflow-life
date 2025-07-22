from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class ActivityType(enum.Enum):
    TRANSPORT = "transport"
    ENERGY = "energy"
    WASTE = "waste"
    SHOPPING = "shopping"

class TransportMode(enum.Enum):
    CAR = "car"
    BUS = "bus"
    SUBWAY = "subway"
    BICYCLE = "bicycle"
    WALKING = "walking"
    AIRPLANE = "airplane"
    TRAIN = "train"

class ActivityLog(Base):
    __tablename__ = "activity_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    activity_type = Column(Enum(ActivityType), nullable=False)
    transport_mode = Column(Enum(TransportMode), nullable=True)
    distance_km = Column(Float, nullable=True)
    energy_usage = Column(Float, nullable=True)  # kWh
    carbon_footprint = Column(Float, nullable=False)  # kg CO2e
    logged_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="activity_logs") 