from app.core.database import Base
from .user import User
from .meal_log import MealLog
from .recommended_swap import RecommendedSwap
from .challenge import Challenge, UserChallenge
from .badge import Badge, UserBadge
from .activity_log import ActivityLog

__all__ = [
    "Base",
    "User", 
    "MealLog", 
    "RecommendedSwap", 
    "Challenge", 
    "UserChallenge",
    "Badge", 
    "UserBadge", 
    "ActivityLog"
] 