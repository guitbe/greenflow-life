from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.meal_log import MealLog
from app.models.recommended_swap import RecommendedSwap

router = APIRouter()

class SwapRecommendation(BaseModel):
    original_food: str
    recommended_food: str
    carbon_reduction: float
    carbon_reduction_percentage: float
    recommendation_message: str
    category: str

class SwapResponse(BaseModel):
    meal_log_id: int
    recommendations: List[SwapRecommendation]

class AcceptSwapRequest(BaseModel):
    swap_id: int
    accepted: bool

@router.get("/{meal_id}", response_model=SwapResponse)
async def get_meal_swap_recommendations(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """식사에 대한 스마트 스왑 추천"""
    
    # Get the meal log
    meal_log = db.query(MealLog).filter(
        MealLog.id == meal_id,
        MealLog.user_id == current_user.id
    ).first()
    
    if not meal_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="식사 기록을 찾을 수 없습니다."
        )
    
    # Generate smart swap recommendations
    recommendations = generate_smart_swaps(
        meal_log.food_name, 
        meal_log.portion_size,
        current_user.dietary_preference
    )
    
    # Save recommendations to database
    for rec in recommendations:
        existing_swap = db.query(RecommendedSwap).filter(
            RecommendedSwap.meal_log_id == meal_id,
            RecommendedSwap.recommended_food == rec.recommended_food
        ).first()
        
        if not existing_swap:
            swap = RecommendedSwap(
                meal_log_id=meal_id,
                original_food=rec.original_food,
                recommended_food=rec.recommended_food,
                carbon_reduction=rec.carbon_reduction,
                recommendation_message=rec.recommendation_message
            )
            db.add(swap)
    
    db.commit()
    
    return SwapResponse(
        meal_log_id=meal_id,
        recommendations=recommendations
    )

@router.post("/accept")
async def accept_swap_recommendation(
    request: AcceptSwapRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """스왑 추천 수락/거절"""
    
    swap = db.query(RecommendedSwap).filter(
        RecommendedSwap.id == request.swap_id
    ).join(MealLog).filter(
        MealLog.user_id == current_user.id
    ).first()
    
    if not swap:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="추천을 찾을 수 없습니다."
        )
    
    swap.accepted = request.accepted
    db.commit()
    
    return {"message": "추천이 업데이트되었습니다.", "accepted": request.accepted}

def generate_smart_swaps(food_name: str, portion_size: float, dietary_preference) -> List[SwapRecommendation]:
    """AI 기반 스마트 식사 대체 추천 로직"""
    
    # 음식별 스마트 스왑 데이터베이스
    swap_database = {
        # 고탄소 육류 → 저탄소 대안
        "소고기": [
            {"swap": "닭고기", "reduction": 1.9, "message": "소고기 대신 닭고기는 어떠세요? 탄소 배출량을 76% 줄일 수 있어요!"},
            {"swap": "두부", "reduction": 2.3, "message": "소고기 대신 두부로 바꿔보세요! 탄소 배출량을 92% 줄일 수 있어요!"},
            {"swap": "콩고기", "reduction": 2.2, "message": "식물성 콩고기로 바꿔보세요! 맛은 비슷하면서 탄소 배출량을 88% 줄일 수 있어요!"}
        ],
        "한우": [
            {"swap": "닭고기", "reduction": 2.2, "message": "한우 대신 닭고기는 어떠세요? 탄소 배출량을 78% 줄일 수 있어요!"},
            {"swap": "생선", "reduction": 2.3, "message": "한우 대신 생선요리는 어떠세요? 탄소 배출량을 82% 줄일 수 있어요!"}
        ],
        "삼겹살": [
            {"swap": "닭가슴살", "reduction": 0.8, "message": "삼겹살 대신 닭가슴살은 어떠세요? 탄소 배출량을 57% 줄일 수 있어요!"},
            {"swap": "연어", "reduction": 0.8, "message": "삼겹살 대신 연어구이는 어떠세요? 탄소 배출량을 57% 줄일 수 있어요!"}
        ],
        
        # 유제품 대안
        "치즈": [
            {"swap": "아몬드 치즈", "reduction": 0.6, "message": "일반 치즈 대신 아몬드 치즈는 어떠세요? 탄소 배출량을 60% 줄일 수 있어요!"},
            {"swap": "두부", "reduction": 0.8, "message": "치즈 대신 두부요리는 어떠세요? 탄소 배출량을 80% 줄일 수 있어요!"}
        ],
        
        # 곡물 대안
        "밥": [
            {"swap": "현미밥", "reduction": 0.1, "message": "흰쌀밥 대신 현미밥은 어떠세요? 탄소 배출량을 33% 줄이고 영양도 더 좋아요!"},
            {"swap": "콩밥", "reduction": 0.05, "message": "밥에 콩을 넣어보세요! 탄소 배출량을 17% 줄이고 단백질도 보충할 수 있어요!"}
        ],
        
        # 해산물 (이미 낮은 탄소이지만 더 나은 옵션)
        "새우": [
            {"swap": "생선", "reduction": 1.3, "message": "새우 대신 생선요리는 어떠세요? 탄소 배출량을 72% 줄일 수 있어요!"},
            {"swap": "조개", "reduction": 1.5, "message": "새우 대신 조개요리는 어떠세요? 탄소 배출량을 83% 줄일 수 있어요!"}
        ]
    }
    
    recommendations = []
    
    # 입력된 음식과 매칭되는 스왑 찾기
    for food_key, swaps in swap_database.items():
        if food_key in food_name:
            for swap_data in swaps:
                # 식단 선호도에 따른 필터링
                if dietary_preference.value == "vegan" and swap_data["swap"] in ["닭고기", "생선", "연어", "닭가슴살"]:
                    continue
                if dietary_preference.value == "vegetarian" and swap_data["swap"] in ["닭고기", "생선", "연어", "닭가슴살"]:
                    continue
                
                carbon_reduction = (portion_size / 100) * swap_data["reduction"]
                original_carbon = calculate_original_carbon(food_name, portion_size)
                reduction_percentage = (carbon_reduction / original_carbon) * 100 if original_carbon > 0 else 0
                
                recommendations.append(SwapRecommendation(
                    original_food=food_name,
                    recommended_food=swap_data["swap"],
                    carbon_reduction=round(carbon_reduction, 3),
                    carbon_reduction_percentage=round(reduction_percentage, 1),
                    recommendation_message=swap_data["message"],
                    category=get_food_category(swap_data["swap"])
                ))
            break
    
    # 일반적인 저탄소 대안 (특정 매칭이 없을 때)
    if not recommendations:
        general_swaps = [
            {"swap": "채소 샐러드", "reduction": 0.4, "message": f"{food_name} 대신 신선한 채소 샐러드는 어떠세요? 탄소 배출량을 크게 줄일 수 있어요!"},
            {"swap": "두부 요리", "reduction": 0.3, "message": f"{food_name} 대신 두부 요리는 어떠세요? 탄소 배출량을 줄이고 건강도 챙길 수 있어요!"}
        ]
        
        for swap_data in general_swaps:
            carbon_reduction = (portion_size / 100) * swap_data["reduction"]
            original_carbon = calculate_original_carbon(food_name, portion_size)
            reduction_percentage = (carbon_reduction / original_carbon) * 100 if original_carbon > 0 else 0
            
            recommendations.append(SwapRecommendation(
                original_food=food_name,
                recommended_food=swap_data["swap"],
                carbon_reduction=round(carbon_reduction, 3),
                carbon_reduction_percentage=round(reduction_percentage, 1),
                recommendation_message=swap_data["message"],
                category="채소"
            ))
    
    return recommendations[:3]  # 최대 3개 추천

def calculate_original_carbon(food_name: str, portion_size: float) -> float:
    """원본 음식의 탄소 발자국 계산"""
    from app.api.footprint import calculate_food_carbon
    return calculate_food_carbon(food_name, portion_size)

def get_food_category(food_name: str) -> str:
    """음식 카테고리 분류"""
    from app.api.footprint import get_food_category as get_category
    return get_category(food_name) 