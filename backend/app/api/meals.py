from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.meal_log import MealLog, MealType

router = APIRouter()

class MealCreate(BaseModel):
    food_name: str
    portion_size: float
    meal_type: MealType
    image_url: Optional[str] = None

class MealResponse(BaseModel):
    id: int
    food_name: str
    portion_size: float
    meal_type: MealType
    carbon_footprint: float
    image_url: Optional[str]
    logged_at: datetime

    class Config:
        from_attributes = True

@router.post("/", response_model=MealResponse)
async def create_meal_log(
    meal_data: MealCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """식사 기록 추가"""
    
    # Calculate carbon footprint (simplified calculation)
    # In real implementation, this would use a comprehensive food database
    carbon_footprint = calculate_carbon_footprint(meal_data.food_name, meal_data.portion_size)
    
    meal_log = MealLog(
        user_id=current_user.id,
        food_name=meal_data.food_name,
        portion_size=meal_data.portion_size,
        meal_type=meal_data.meal_type,
        carbon_footprint=carbon_footprint,
        image_url=meal_data.image_url
    )
    
    db.add(meal_log)
    db.commit()
    db.refresh(meal_log)
    
    return meal_log

@router.get("/", response_model=List[MealResponse])
async def get_meal_logs(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """식사 기록 조회"""
    
    meal_logs = db.query(MealLog).filter(
        MealLog.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    
    return meal_logs

@router.get("/{meal_id}", response_model=MealResponse)
async def get_meal_log(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """특정 식사 기록 조회"""
    
    meal_log = db.query(MealLog).filter(
        MealLog.id == meal_id,
        MealLog.user_id == current_user.id
    ).first()
    
    if not meal_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="식사 기록을 찾을 수 없습니다."
        )
    
    return meal_log

def calculate_carbon_footprint(food_name: str, portion_size: float) -> float:
    """
    음식의 탄소 발자국 계산 (간단한 예시)
    실제 구현에서는 포괄적인 음식 데이터베이스를 사용해야 함
    """
    # Simplified carbon footprint database (kg CO2e per 100g)
    carbon_factors = {
        "소고기": 2.5,
        "돼지고기": 1.2,
        "닭고기": 0.6,
        "생선": 0.5,
        "달걀": 0.4,
        "쌀": 0.3,
        "면": 0.2,
        "채소": 0.1,
        "과일": 0.1,
    }
    
    # Find matching food category
    for food, factor in carbon_factors.items():
        if food in food_name:
            return (portion_size / 100) * factor
    
    # Default factor for unknown foods
    return (portion_size / 100) * 0.5 