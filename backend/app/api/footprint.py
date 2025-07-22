from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.meal_log import MealLog

router = APIRouter()

class CarbonCalculationRequest(BaseModel):
    food_name: str
    portion_size: float  # in grams

class CarbonCalculationResponse(BaseModel):
    food_name: str
    portion_size: float
    carbon_footprint: float  # kg CO2e
    category: str
    sustainability_rating: str  # LOW, MEDIUM, HIGH

class DailySummary(BaseModel):
    date: str
    total_carbon: float
    meal_count: int
    top_contributor: str

@router.post("/calculate", response_model=CarbonCalculationResponse)
async def calculate_carbon_footprint(
    request: CarbonCalculationRequest,
    current_user: User = Depends(get_current_user)
):
    """탄소 발자국 계산"""
    
    carbon_footprint = calculate_food_carbon(request.food_name, request.portion_size)
    category = get_food_category(request.food_name)
    rating = get_sustainability_rating(carbon_footprint)
    
    return CarbonCalculationResponse(
        food_name=request.food_name,
        portion_size=request.portion_size,
        carbon_footprint=carbon_footprint,
        category=category,
        sustainability_rating=rating
    )

@router.get("/daily-summary", response_model=List[DailySummary])
async def get_daily_carbon_summary(
    days: int = 7,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """일별 탄소 발자국 요약"""
    
    from sqlalchemy import func, desc
    from datetime import datetime, timedelta
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Get daily aggregated data
    daily_data = db.query(
        func.date(MealLog.logged_at).label('date'),
        func.sum(MealLog.carbon_footprint).label('total_carbon'),
        func.count(MealLog.id).label('meal_count'),
        func.max(MealLog.carbon_footprint).label('max_carbon')
    ).filter(
        MealLog.user_id == current_user.id,
        MealLog.logged_at >= start_date,
        MealLog.logged_at <= end_date
    ).group_by(
        func.date(MealLog.logged_at)
    ).order_by(desc('date')).all()
    
    result = []
    for data in daily_data:
        # Get the food with highest carbon footprint for that day
        top_meal = db.query(MealLog).filter(
            MealLog.user_id == current_user.id,
            func.date(MealLog.logged_at) == data.date,
            MealLog.carbon_footprint == data.max_carbon
        ).first()
        
        result.append(DailySummary(
            date=data.date.strftime("%Y-%m-%d"),
            total_carbon=round(data.total_carbon, 2),
            meal_count=data.meal_count,
            top_contributor=top_meal.food_name if top_meal else "알 수 없음"
        ))
    
    return result

def calculate_food_carbon(food_name: str, portion_size: float) -> float:
    """음식의 탄소 발자국 계산 - 한국 특화 데이터 사용"""
    from app.data.korean_food_carbon import get_food_carbon_footprint, search_similar_foods
    
    # 1. 정확한 매칭 시도
    exact_footprint = get_food_carbon_footprint(food_name, portion_size / 200.0)  # 200g을 1인분으로 가정
    if exact_footprint != 1.0 * (portion_size / 200.0):  # 기본값이 아닌 경우
        return round(exact_footprint, 3)
    
    # 2. 유사한 음식 검색
    similar_foods = search_similar_foods(food_name)
    if similar_foods:
        # 가장 유사한 음식의 탄소 발자국 사용
        base_footprint = similar_foods[0]["carbon_footprint"]
        return round(base_footprint * (portion_size / 200.0), 3)
    
    # 3. 기존 로직 fallback (간단한 카테고리 매칭)
    carbon_factors_per_100g = {
        # 육류 키워드
        "소": 2.5, "돼지": 1.2, "닭": 0.6, "양": 2.4,
        "고기": 2.0, "갈비": 2.8, "등심": 2.6,
        
        # 해산물 키워드
        "생선": 0.5, "새우": 1.8, "게": 1.5, "조개": 0.3,
        "회": 1.0, "초밥": 0.9,
        
        # 기타
        "밥": 0.3, "면": 0.2, "국": 0.5, "찌개": 0.4,
        "채소": 0.1, "과일": 0.1, "두부": 0.2
    }
    
    best_match_factor = 0.5  # 기본값
    for keyword, factor in carbon_factors_per_100g.items():
        if keyword in food_name:
            best_match_factor = factor
            break
    
    return round((portion_size / 100) * best_match_factor, 3)

def get_food_category(food_name: str) -> str:
    """음식 카테고리 분류"""
    categories = {
        "육류": ["소고기", "돼지고기", "닭고기", "양고기", "한우", "삼겹살", "치킨"],
        "해산물": ["생선", "새우", "게", "조개", "굴", "연어", "참치"],
        "유제품": ["우유", "치즈", "버터", "요거트", "달걀"],
        "곡물": ["쌀", "밥", "빵", "면", "파스타"],
        "채소": ["채소", "상추", "양배추", "브로콜리", "당근", "감자"],
        "과일": ["과일", "사과", "바나나", "오렌지", "포도", "딸기"],
        "기타": ["두부", "콩", "커피", "차", "견과류"]
    }
    
    for category, foods in categories.items():
        for food in foods:
            if food in food_name:
                return category
    
    return "기타"

def get_sustainability_rating(carbon_footprint: float) -> str:
    """지속가능성 등급 평가"""
    if carbon_footprint < 0.5:
        return "HIGH"  # 높은 지속가능성
    elif carbon_footprint < 1.5:
        return "MEDIUM"  # 보통 지속가능성
    else:
        return "LOW"  # 낮은 지속가능성 