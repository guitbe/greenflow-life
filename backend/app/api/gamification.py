from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.meal_log import MealLog
from app.models.challenge import Challenge, UserChallenge
from app.models.badge import Badge, UserBadge
from app.models.recommended_swap import RecommendedSwap
from app.utils.korean_messages import korean_messages

router = APIRouter()

class AchievementResponse(BaseModel):
    id: str
    type: str
    title: str
    message: str
    icon: str
    points: int
    rarity: str
    achieved_at: datetime

class PersonalizedChallengeResponse(BaseModel):
    id: int
    title: str
    description: str
    korean_message: str
    target_value: int
    current_progress: int
    progress_percentage: float
    reward_points: int
    difficulty: str
    estimated_days: int
    is_achievable: bool

class GameStatsResponse(BaseModel):
    level: int
    level_title: str
    total_points: int
    points_to_next_level: int
    current_streak: int
    best_streak: int
    total_carbon_saved: float
    achievement_count: int
    challenge_completion_rate: float

@router.get("/achievements/recent", response_model=List[AchievementResponse])
async def get_recent_achievements(
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """최근 달성한 성취 목록 조회"""
    
    recent_badges = db.query(UserBadge).join(Badge).filter(
        UserBadge.user_id == current_user.id
    ).order_by(UserBadge.earned_at.desc()).limit(limit).all()
    
    achievements = []
    for user_badge in recent_badges:
        achievements.append(AchievementResponse(
            id=f"badge_{user_badge.badge_id}",
            type="badge",
            title=user_badge.badge.name,
            message=korean_messages.get_success_message("challenge_completed"),
            icon=get_badge_emoji(user_badge.badge.badge_type),
            points=getattr(user_badge.badge, 'points', 100),
            rarity=get_badge_rarity(user_badge.badge.badge_type),
            achieved_at=user_badge.earned_at
        ))
    
    return achievements

@router.get("/challenges/personalized", response_model=List[PersonalizedChallengeResponse])
async def get_personalized_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 맞춤형 개인화된 챌린지 추천"""
    
    # 사용자의 최근 활동 패턴 분석
    recent_meals = db.query(MealLog).filter(
        MealLog.user_id == current_user.id
    ).order_by(MealLog.logged_at.desc()).limit(20).all()
    
    user_patterns = analyze_user_meal_patterns(recent_meals)
    
    # 기본 챌린지 생성
    personalized_challenges = []
    
    # 1. 연속 기록 챌린지
    current_streak = calculate_current_streak(current_user.id, db)
    if current_streak < 7:
        target_days = 7 if current_streak < 3 else 14
        personalized_challenges.append({
            "title": f"{target_days}일 연속 기록 챌린지",
            "description": f"{target_days}일 동안 매일 식사를 기록해보세요!",
            "korean_message": f"매일 기록하는 습관, {target_days}일 도전! 꾸준함이 가장 큰 힘이에요 💪",
            "target_value": target_days,
            "current_progress": current_streak,
            "reward_points": target_days * 50,
            "difficulty": "easy" if target_days == 7 else "medium",
            "estimated_days": target_days - current_streak,
            "type": "streak"
        })
    
    # 2. 탄소 절약 챌린지 (패턴 기반)
    avg_carbon = user_patterns.get("avg_carbon_per_meal", 3.0)
    if avg_carbon > 2.0:
        target_reduction = min(avg_carbon * 0.3, 2.0)  # 30% 감소 또는 최대 2kg
        personalized_challenges.append({
            "title": "스마트 탄소 절약 챌린지",
            "description": f"이번 주 평균 식사당 {target_reduction:.1f}kg 탄소 절약하기",
            "korean_message": f"지금보다 조금만 더! 평균 {target_reduction:.1f}kg만 줄이면 지구가 더 건강해져요 🌍",
            "target_value": int(target_reduction * 10),  # 0.1kg 단위로 저장
            "current_progress": 0,
            "reward_points": 300,
            "difficulty": "medium",
            "estimated_days": 7,
            "type": "carbon_reduction"
        })
    
    # 3. 다양성 챌린지
    variety_score = user_patterns.get("variety_score", 0.5)
    if variety_score < 0.6:
        personalized_challenges.append({
            "title": "다양한 맛 탐험 챌린지",
            "description": "이번 주에 5가지 다른 카테고리 음식 시도하기",
            "korean_message": "새로운 맛의 발견! 다양한 음식으로 미식 여행을 떠나보세요 🌈",
            "target_value": 5,
            "current_progress": 0,
            "reward_points": 200,
            "difficulty": "easy",
            "estimated_days": 7,
            "type": "variety"
        })
    
    # 4. 스마트 스왑 챌린지
    recent_swaps = db.query(RecommendedSwap).join(MealLog).filter(
        MealLog.user_id == current_user.id,
        RecommendedSwap.created_at >= datetime.now() - timedelta(days=30)
    ).count()
    
    if recent_swaps < 5:
        personalized_challenges.append({
            "title": "친환경 선택 마스터 챌린지",
            "description": "이번 주에 스마트 스왑 추천 3번 수락하기",
            "korean_message": "현명한 선택의 연속! 스마트 스왑으로 환경 히어로가 되어보세요 ⚡",
            "target_value": 3,
            "current_progress": 0,
            "reward_points": 250,
            "difficulty": "medium",
            "estimated_days": 7,
            "type": "smart_swap"
        })
    
    # PersonalizedChallengeResponse 형태로 변환
    response_challenges = []
    for i, challenge in enumerate(personalized_challenges):
        response_challenges.append(PersonalizedChallengeResponse(
            id=1000 + i,  # 임시 ID (실제로는 DB에서 생성)
            title=challenge["title"],
            description=challenge["description"],
            korean_message=challenge["korean_message"],
            target_value=challenge["target_value"],
            current_progress=challenge["current_progress"],
            progress_percentage=(challenge["current_progress"] / challenge["target_value"]) * 100,
            reward_points=challenge["reward_points"],
            difficulty=challenge["difficulty"],
            estimated_days=challenge["estimated_days"],
            is_achievable=challenge["estimated_days"] <= 14  # 2주 이내 달성 가능한 것만
        ))
    
    return response_challenges

@router.get("/stats", response_model=GameStatsResponse)
async def get_game_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게이미피케이션 통계 조회"""
    
    # 총 포인트 계산 (배지 기반)
    total_points = db.query(func.sum(Badge.points)).join(UserBadge).filter(
        UserBadge.user_id == current_user.id
    ).scalar() or 0
    
    # 레벨 계산
    level_info = calculate_user_level(total_points)
    
    # 연속 기록 계산
    current_streak = calculate_current_streak(current_user.id, db)
    best_streak = calculate_best_streak(current_user.id, db)
    
    # 총 탄소 절약량
    total_carbon_saved = db.query(func.sum(RecommendedSwap.carbon_reduction)).join(
        MealLog
    ).filter(
        MealLog.user_id == current_user.id,
        RecommendedSwap.accepted == True
    ).scalar() or 0.0
    
    # 성취 개수
    achievement_count = db.query(func.count(UserBadge.id)).filter(
        UserBadge.user_id == current_user.id
    ).scalar() or 0
    
    # 챌린지 완료율
    total_challenges = db.query(func.count(UserChallenge.id)).filter(
        UserChallenge.user_id == current_user.id
    ).scalar() or 0
    
    completed_challenges = db.query(func.count(UserChallenge.id)).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.completed == True
    ).scalar() or 0
    
    completion_rate = (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0
    
    return GameStatsResponse(
        level=level_info["level"],
        level_title=level_info["title"],
        total_points=total_points,
        points_to_next_level=level_info["points_to_next"] - total_points if level_info["points_to_next"] else 0,
        current_streak=current_streak,
        best_streak=best_streak,
        total_carbon_saved=round(total_carbon_saved, 2),
        achievement_count=achievement_count,
        challenge_completion_rate=round(completion_rate, 1)
    )

@router.post("/trigger-achievement")
async def trigger_achievement(
    achievement_type: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """성취 달성 트리거 (게임 로직에서 호출)"""
    
    achievement_rules = {
        "first_meal": {
            "condition": lambda: db.query(MealLog).filter(MealLog.user_id == current_user.id).count() == 1,
            "badge_type": "first_meal",
            "message": korean_messages.get_success_message("meal_logged") + " 첫 기록을 축하해요! 🎉"
        },
        "week_streak": {
            "condition": lambda: calculate_current_streak(current_user.id, db) >= 7,
            "badge_type": "week_streak", 
            "message": "7일 연속 기록! 꾸준함의 힘을 보여주고 계시네요! 🔥"
        },
        "carbon_saver": {
            "condition": lambda: db.query(func.sum(RecommendedSwap.carbon_reduction)).join(MealLog).filter(
                MealLog.user_id == current_user.id, RecommendedSwap.accepted == True
            ).scalar() >= 10.0,
            "badge_type": "carbon_saver",
            "message": "10kg 탄소 절약 달성! 정말 대단한 환경 지킨이에요! 🌱"
        }
    }
    
    rule = achievement_rules.get(achievement_type)
    if not rule:
        raise HTTPException(status_code=400, detail="Unknown achievement type")
    
    # 조건 체크
    if not rule["condition"]():
        raise HTTPException(status_code=400, detail="Achievement condition not met")
    
    # 이미 획득했는지 체크
    existing_badge = db.query(UserBadge).join(Badge).filter(
        UserBadge.user_id == current_user.id,
        Badge.badge_type == rule["badge_type"]
    ).first()
    
    if existing_badge:
        raise HTTPException(status_code=400, detail="Achievement already earned")
    
    # 배지 생성 및 부여
    badge = db.query(Badge).filter(Badge.badge_type == rule["badge_type"]).first()
    if not badge:
        # 배지가 없으면 생성
        badge = Badge(
            name=get_badge_name(rule["badge_type"]),
            description=get_badge_description(rule["badge_type"]),
            badge_type=rule["badge_type"],
            icon=get_badge_emoji(rule["badge_type"]),
            points=get_badge_points(rule["badge_type"])
        )
        db.add(badge)
        db.commit()
        db.refresh(badge)
    
    # 사용자 배지 생성
    user_badge = UserBadge(
        user_id=current_user.id,
        badge_id=badge.id
    )
    db.add(user_badge)
    db.commit()
    
    return {
        "success": True,
        "achievement": {
            "title": badge.name,
            "message": rule["message"],
            "icon": badge.icon,
            "points": badge.points
        }
    }

@router.post("/progress-update")
async def update_progress(
    activity_type: str,
    value: float,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """진행 상황 업데이트 및 자동 성취 체크"""
    
    responses = []
    
    # 활동에 따른 자동 성취 체크
    if activity_type == "meal_logged":
        meal_count = db.query(func.count(MealLog.id)).filter(
            MealLog.user_id == current_user.id
        ).scalar()
        
        # 첫 식사 기록
        if meal_count == 1:
            try:
                achievement = await trigger_achievement("first_meal", current_user, db)
                responses.append(achievement)
            except HTTPException:
                pass
        
        # 연속 기록 체크
        current_streak = calculate_current_streak(current_user.id, db)
        if current_streak == 7:
            try:
                achievement = await trigger_achievement("week_streak", current_user, db)
                responses.append(achievement)
            except HTTPException:
                pass
                
    elif activity_type == "swap_accepted":
        # 탄소 절약 성취 체크
        total_saved = db.query(func.sum(RecommendedSwap.carbon_reduction)).join(MealLog).filter(
            MealLog.user_id == current_user.id,
            RecommendedSwap.accepted == True
        ).scalar() or 0.0
        
        if total_saved >= 10.0:
            try:
                achievement = await trigger_achievement("carbon_saver", current_user, db)
                responses.append(achievement)
            except HTTPException:
                pass
    
    return {
        "success": True,
        "triggered_achievements": responses,
        "motivational_message": korean_messages.get_tip_message()
    }

# 헬퍼 함수들
def calculate_current_streak(user_id: int, db: Session) -> int:
    """현재 연속 기록 일수 계산"""
    meals = db.query(MealLog).filter(
        MealLog.user_id == user_id
    ).order_by(MealLog.logged_at.desc()).all()
    
    if not meals:
        return 0
    
    dates = [meal.logged_at.date() for meal in meals]
    unique_dates = sorted(set(dates), reverse=True)
    
    if not unique_dates:
        return 0
    
    # 오늘부터 연속으로 기록한 날 계산
    today = datetime.now().date()
    streak = 0
    
    for i, date in enumerate(unique_dates):
        expected_date = today - timedelta(days=i)
        if date == expected_date:
            streak += 1
        else:
            break
    
    return streak

def calculate_best_streak(user_id: int, db: Session) -> int:
    """최고 연속 기록 일수 계산"""
    meals = db.query(MealLog).filter(
        MealLog.user_id == user_id
    ).order_by(MealLog.logged_at).all()
    
    if not meals:
        return 0
    
    dates = [meal.logged_at.date() for meal in meals]
    unique_dates = sorted(set(dates))
    
    if not unique_dates:
        return 0
    
    max_streak = 1
    current_streak = 1
    
    for i in range(1, len(unique_dates)):
        if (unique_dates[i] - unique_dates[i-1]).days == 1:
            current_streak += 1
            max_streak = max(max_streak, current_streak)
        else:
            current_streak = 1
    
    return max_streak

def calculate_user_level(total_points: int) -> dict:
    """사용자 레벨 계산"""
    level_thresholds = [
        (0, "새싹 지킴이", 500),
        (500, "친환경 실천가", 1500),
        (1500, "탄소 절약자", 3000),
        (3000, "환경 전문가", 5000),
        (5000, "지구 지킴이", 10000),
        (10000, "환경 마스터", None)
    ]
    
    for i, (threshold, title, next_threshold) in enumerate(level_thresholds):
        if total_points >= threshold and (next_threshold is None or total_points < next_threshold):
            return {
                "level": i + 1,
                "title": title,
                "points_to_next": next_threshold
            }
    
    return {"level": 1, "title": "새싹 지킴이", "points_to_next": 500}

def analyze_user_meal_patterns(meals: List[MealLog]) -> dict:
    """간단한 사용자 식사 패턴 분석"""
    if not meals:
        return {"avg_carbon_per_meal": 0, "variety_score": 0}
    
    total_carbon = sum(meal.carbon_footprint for meal in meals)
    avg_carbon = total_carbon / len(meals)
    
    # 음식 다양성 (유니크한 음식 수 / 총 식사 수)
    unique_foods = len(set(meal.food_name for meal in meals))
    variety_score = unique_foods / len(meals)
    
    return {
        "avg_carbon_per_meal": avg_carbon,
        "variety_score": variety_score
    }

def get_badge_emoji(badge_type: str) -> str:
    """배지 타입별 이모지 반환"""
    emoji_map = {
        "first_meal": "🍽️",
        "week_streak": "🔥",
        "month_streak": "👑",
        "carbon_saver": "🌱",
        "eco_warrior": "🌍",
        "smart_swapper": "⚡",
        "challenge_master": "🏆"
    }
    return emoji_map.get(badge_type, "🏅")

def get_badge_name(badge_type: str) -> str:
    """배지 타입별 이름 반환"""
    name_map = {
        "first_meal": "첫 기록의 주인공",
        "week_streak": "일주일 연속 달성자",
        "month_streak": "한달 연속 마스터",
        "carbon_saver": "탄소 절약 영웅", 
        "eco_warrior": "환경 전사",
        "smart_swapper": "스마트 선택 마스터",
        "challenge_master": "챌린지 정복자"
    }
    return name_map.get(badge_type, "특별한 성취")

def get_badge_description(badge_type: str) -> str:
    """배지 타입별 설명 반환"""
    desc_map = {
        "first_meal": "첫 번째 식사를 기록한 특별한 순간",
        "week_streak": "7일 연속으로 꾸준히 기록한 의지력의 증거",
        "month_streak": "30일 연속 기록의 놀라운 끈기",
        "carbon_saver": "10kg 이상의 탄소를 절약한 환경 지킴이",
        "eco_warrior": "지속적인 친환경 실천의 진정한 용사",
        "smart_swapper": "현명한 식단 선택으로 변화를 만드는 리더",
        "challenge_master": "다양한 챌린지를 완수한 도전의 달인"
    }
    return desc_map.get(badge_type, "특별한 성취를 달성했습니다")

def get_badge_points(badge_type: str) -> int:
    """배지 타입별 포인트 반환"""
    points_map = {
        "first_meal": 100,
        "week_streak": 300,
        "month_streak": 1000,
        "carbon_saver": 500,
        "eco_warrior": 1500,
        "smart_swapper": 400,
        "challenge_master": 800
    }
    return points_map.get(badge_type, 100)

def get_badge_rarity(badge_type: str) -> str:
    """배지 희귀도 반환"""
    rarity_map = {
        "first_meal": "common",
        "week_streak": "rare", 
        "month_streak": "epic",
        "carbon_saver": "rare",
        "eco_warrior": "legendary",
        "smart_swapper": "rare",
        "challenge_master": "epic"
    }
    return rarity_map.get(badge_type, "common") 