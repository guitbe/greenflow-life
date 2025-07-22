from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.core.database import Base

class ChallengeType(enum.Enum):
    CARBON_REDUCTION = "carbon_reduction"
    MEAL_LOGGING = "meal_logging"
    SWAP_ACCEPTANCE = "swap_acceptance"
    WEEKLY_GOAL = "weekly_goal"

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    challenge_type = Column(Enum(ChallengeType), nullable=False)
    target_value = Column(Integer, nullable=False)
    badge_icon = Column(String, nullable=True)
    duration_days = Column(Integer, default=30)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user_challenges = relationship("UserChallenge", back_populates="challenge")

class UserChallenge(Base):
    __tablename__ = "user_challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    current_progress = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="user_challenges")
    challenge = relationship("Challenge", back_populates="user_challenges") 