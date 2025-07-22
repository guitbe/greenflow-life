from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.meal_log import MealLog
from app.models.recommended_swap import RecommendedSwap
from app.models.challenge import UserChallenge, Challenge

router = APIRouter()

class DashboardStats(BaseModel):
    total_carbon_this_week: float
    carbon_reduction_achieved: float
    target_progress_percentage: float
    meals_logged_this_week: int
    swaps_accepted: int
    active_challenges: int
    completed_challenges: int

class CarbonTrend(BaseModel):
    date: str
    carbon_amount: float
    meal_count: int

class TopContributor(BaseModel):
    food_name: str
    total_carbon: float
    frequency: int

class InsightCard(BaseModel):
    type: str  # "achievement", "tip", "warning", "celebration"
    title: str
    message: str
    icon: str
    action_text: str

class DashboardResponse(BaseModel):
    stats: DashboardStats
    carbon_trends: List[CarbonTrend]
    top_contributors: List[TopContributor]
    insights: List[InsightCard]

@router.get("/", response_model=DashboardResponse)
async def get_dashboard_data(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """대시보드 통계 데이터 조회"""
    
    # Calculate date ranges
    now = datetime.now()
    week_start = now - timedelta(days=7)
    month_start = now - timedelta(days=30)
    
    # Basic stats
    stats = calculate_dashboard_stats(db, current_user.id, week_start, month_start)
    
    # Carbon trends (last 7 days)
    carbon_trends = get_carbon_trends(db, current_user.id, week_start)
    
    # Top carbon contributors
    top_contributors = get_top_contributors(db, current_user.id, month_start)
    
    # Generate insights
    insights = generate_insights(db, current_user, stats, carbon_trends)
    
    return DashboardResponse(
        stats=stats,
        carbon_trends=carbon_trends,
        top_contributors=top_contributors,
        insights=insights
    )

def calculate_dashboard_stats(db: Session, user_id: int, week_start: datetime, month_start: datetime) -> DashboardStats:
    """대시보드 기본 통계 계산"""
    
    # This week's carbon footprint
    week_carbon = db.query(func.sum(MealLog.carbon_footprint)).filter(
        MealLog.user_id == user_id,
        MealLog.logged_at >= week_start
    ).scalar() or 0.0
    
    # Carbon reduction from accepted swaps
    carbon_reduction = db.query(func.sum(RecommendedSwap.carbon_reduction)).join(
        MealLog
    ).filter(
        MealLog.user_id == user_id,
        RecommendedSwap.accepted == True,
        RecommendedSwap.created_at >= month_start
    ).scalar() or 0.0
    
    # Meals logged this week
    meals_count = db.query(func.count(MealLog.id)).filter(
        MealLog.user_id == user_id,
        MealLog.logged_at >= week_start
    ).scalar() or 0
    
    # Swaps accepted
    swaps_accepted = db.query(func.count(RecommendedSwap.id)).join(
        MealLog
    ).filter(
        MealLog.user_id == user_id,
        RecommendedSwap.accepted == True,
        RecommendedSwap.created_at >= month_start
    ).scalar() or 0
    
    # Challenges
    active_challenges = db.query(func.count(UserChallenge.id)).filter(
        UserChallenge.user_id == user_id,
        UserChallenge.completed == False
    ).scalar() or 0
    
    completed_challenges = db.query(func.count(UserChallenge.id)).filter(
        UserChallenge.user_id == user_id,
        UserChallenge.completed == True
    ).scalar() or 0
    
    # Calculate target progress (assuming 20% reduction target)
    target_carbon = week_carbon * 1.25  # If they reduced by 20%, original would be 25% higher
    target_progress = min(100, (carbon_reduction / (target_carbon * 0.2)) * 100) if target_carbon > 0 else 0
    
    return DashboardStats(
        total_carbon_this_week=round(week_carbon, 2),
        carbon_reduction_achieved=round(carbon_reduction, 2),
        target_progress_percentage=round(target_progress, 1),
        meals_logged_this_week=meals_count,
        swaps_accepted=swaps_accepted,
        active_challenges=active_challenges,
        completed_challenges=completed_challenges
    )

def get_carbon_trends(db: Session, user_id: int, week_start: datetime) -> List[CarbonTrend]:
    """주간 탄소 발자국 트렌드"""
    
    daily_data = db.query(
        func.date(MealLog.logged_at).label('date'),
        func.sum(MealLog.carbon_footprint).label('total_carbon'),
        func.count(MealLog.id).label('meal_count')
    ).filter(
        MealLog.user_id == user_id,
        MealLog.logged_at >= week_start
    ).group_by(
        func.date(MealLog.logged_at)
    ).order_by('date').all()
    
    trends = []
    for data in daily_data:
        trends.append(CarbonTrend(
            date=data.date.strftime("%Y-%m-%d"),
            carbon_amount=round(data.total_carbon, 2),
            meal_count=data.meal_count
        ))
    
    return trends

def get_top_contributors(db: Session, user_id: int, month_start: datetime) -> List[TopContributor]:
    """탄소 배출량 상위 기여 음식"""
    
    top_foods = db.query(
        MealLog.food_name,
        func.sum(MealLog.carbon_footprint).label('total_carbon'),
        func.count(MealLog.id).label('frequency')
    ).filter(
        MealLog.user_id == user_id,
        MealLog.logged_at >= month_start
    ).group_by(
        MealLog.food_name
    ).order_by(
        desc('total_carbon')
    ).limit(5).all()
    
    contributors = []
    for food_data in top_foods:
        contributors.append(TopContributor(
            food_name=food_data.food_name,
            total_carbon=round(food_data.total_carbon, 2),
            frequency=food_data.frequency
        ))
    
    return contributors

def generate_insights(db: Session, user: User, stats: DashboardStats, trends: List[CarbonTrend]) -> List[InsightCard]:
    """개인화된 인사이트 카드 생성"""
    
    insights = []
    
    # Achievement insights
    if stats.swaps_accepted > 0:
        insights.append(InsightCard(
            type="achievement",
            title="훌륭해요! 🎉",
            message=f"이번 달에 {stats.swaps_accepted}개의 스마트 스왑을 실천하여 {stats.carbon_reduction_achieved}kg의 탄소를 절약했어요!",
            icon="🌱",
            action_text="더 많은 스왑 보기"
        ))
    
    # Progress insights
    if stats.target_progress_percentage >= 50:
        insights.append(InsightCard(
            type="celebration",
            title="목표 달성 중! 💪",
            message=f"탄소 감축 목표의 {stats.target_progress_percentage}%를 달성했어요! 계속 화이팅!",
            icon="🎯",
            action_text="목표 조정하기"
        ))
    elif stats.target_progress_percentage < 25:
        insights.append(InsightCard(
            type="tip",
            title="더 노력해봐요! 📈",
            message="아직 목표까지 조금 더 노력이 필요해요. 스마트 스왑을 더 활용해보시는 건 어떨까요?",
            icon="💡",
            action_text="스왑 추천 보기"
        ))
    
    # Trend insights
    if len(trends) >= 3:
        recent_carbon = sum(t.carbon_amount for t in trends[-3:]) / 3
        earlier_carbon = sum(t.carbon_amount for t in trends[:3]) / 3 if len(trends) >= 6 else recent_carbon
        
        if recent_carbon < earlier_carbon * 0.9:
            insights.append(InsightCard(
                type="achievement",
                title="감소 추세 확인! 📉",
                message="최근 3일간 탄소 배출량이 줄어들고 있어요. 이 추세를 계속 유지해보세요!",
                icon="📉",
                action_text="트렌드 자세히 보기"
            ))
        elif recent_carbon > earlier_carbon * 1.1:
            insights.append(InsightCard(
                type="warning",
                title="주의가 필요해요 ⚠️",
                message="최근 탄소 배출량이 증가하고 있어요. 식단을 다시 점검해보시는 건 어떨까요?",
                icon="⚠️",
                action_text="식단 분석하기"
            ))
    
    # Challenge insights
    if stats.active_challenges == 0:
        insights.append(InsightCard(
            type="tip",
            title="새로운 도전! 🏆",
            message="새로운 챌린지에 참여해서 더 재미있게 탄소 발자국을 줄여보세요!",
            icon="🏆",
            action_text="챌린지 둘러보기"
        ))
    
    return insights[:4]  # 최대 4개 인사이트 반환

def analyze_user_patterns(recent_meals: List[MealLog]) -> dict:
    """사용자의 식사 패턴 상세 분석"""
    from app.data.korean_food_carbon import get_food_category, KOREAN_FOOD_CARBON_DB
    from collections import Counter
    import datetime
    
    if not recent_meals:
        return {
            "frequent_category": "다양한",
            "high_carbon_ratio": 0.0,
            "frequent_high_carbon": False,
            "streak_days": 0,
            "variety_score": 0.0
        }
    
    # 음식 카테고리 분석
    categories = [get_food_category(meal.food_name) for meal in recent_meals]
    category_counter = Counter(categories)
    most_frequent_category = category_counter.most_common(1)[0][0] if category_counter else "다양한"
    
    # 고탄소 음식 비율 계산
    high_carbon_meals = 0
    total_carbon = 0
    
    for meal in recent_meals:
        meal_carbon = KOREAN_FOOD_CARBON_DB.get(meal.food_name, meal.carbon_footprint)
        total_carbon += meal_carbon
        if meal_carbon > 5.0:  # 5kg 이상을 고탄소로 분류
            high_carbon_meals += 1
    
    high_carbon_ratio = high_carbon_meals / len(recent_meals) if recent_meals else 0
    
    # 연속 기록 일수 (간단한 계산)
    dates = [meal.logged_at.date() for meal in recent_meals]
    unique_dates = sorted(set(dates), reverse=True)
    
    streak_days = 1
    if len(unique_dates) > 1:
        for i in range(len(unique_dates) - 1):
            if (unique_dates[i] - unique_dates[i + 1]).days == 1:
                streak_days += 1
            else:
                break
    
    # 다양성 점수 (카테고리 수 / 총 식사 수)
    variety_score = len(set(categories)) / len(recent_meals) if recent_meals else 0
    
    return {
        "frequent_category": most_frequent_category,
        "high_carbon_ratio": high_carbon_ratio,
        "frequent_high_carbon": high_carbon_ratio > 0.5,
        "streak_days": streak_days,
        "variety_score": variety_score,
        "total_meals": len(recent_meals),
        "avg_carbon_per_meal": total_carbon / len(recent_meals) if recent_meals else 0
    } 