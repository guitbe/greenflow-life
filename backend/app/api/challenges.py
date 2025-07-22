from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.challenge import Challenge, UserChallenge, ChallengeType

router = APIRouter()

class ChallengeResponse(BaseModel):
    id: int
    name: str
    description: str
    challenge_type: ChallengeType
    target_value: int
    badge_icon: Optional[str]
    duration_days: int
    is_active: bool

    class Config:
        from_attributes = True

class UserChallengeResponse(BaseModel):
    id: int
    challenge: ChallengeResponse
    current_progress: int
    completed: bool
    progress_percentage: float
    started_at: datetime
    completed_at: Optional[datetime]
    days_remaining: int

class JoinChallengeRequest(BaseModel):
    challenge_id: int

class UpdateProgressRequest(BaseModel):
    challenge_id: int
    progress_value: int

@router.get("/available", response_model=List[ChallengeResponse])
async def get_available_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """참여 가능한 챌린지 목록 조회"""
    
    # Get challenges that user hasn't joined yet
    joined_challenge_ids = db.query(UserChallenge.challenge_id).filter(
        UserChallenge.user_id == current_user.id
    ).subquery()
    
    available_challenges = db.query(Challenge).filter(
        Challenge.is_active == True,
        ~Challenge.id.in_(joined_challenge_ids)
    ).all()
    
    return available_challenges

@router.get("/my-challenges", response_model=List[UserChallengeResponse])
async def get_my_challenges(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 챌린지 목록 조회"""
    
    user_challenges = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id
    ).join(Challenge).all()
    
    result = []
    for uc in user_challenges:
        progress_percentage = min(100, (uc.current_progress / uc.challenge.target_value) * 100)
        
        # Calculate days remaining
        end_date = uc.started_at + timedelta(days=uc.challenge.duration_days)
        days_remaining = max(0, (end_date - datetime.utcnow()).days)
        
        result.append(UserChallengeResponse(
            id=uc.id,
            challenge=uc.challenge,
            current_progress=uc.current_progress,
            completed=uc.completed,
            progress_percentage=round(progress_percentage, 1),
            started_at=uc.started_at,
            completed_at=uc.completed_at,
            days_remaining=days_remaining
        ))
    
    return result

@router.post("/join")
async def join_challenge(
    request: JoinChallengeRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """챌린지 참여"""
    
    # Check if challenge exists and is active
    challenge = db.query(Challenge).filter(
        Challenge.id == request.challenge_id,
        Challenge.is_active == True
    ).first()
    
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="챌린지를 찾을 수 없습니다."
        )
    
    # Check if user already joined this challenge
    existing = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == request.challenge_id
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 참여한 챌린지입니다."
        )
    
    # Create user challenge
    user_challenge = UserChallenge(
        user_id=current_user.id,
        challenge_id=request.challenge_id,
        current_progress=0,
        completed=False
    )
    
    db.add(user_challenge)
    db.commit()
    
    return {"message": "챌린지에 성공적으로 참여했습니다!", "challenge_name": challenge.name}

@router.patch("/update-progress")
async def update_challenge_progress(
    request: UpdateProgressRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """챌린지 진행 상황 업데이트"""
    
    user_challenge = db.query(UserChallenge).filter(
        UserChallenge.user_id == current_user.id,
        UserChallenge.challenge_id == request.challenge_id,
        UserChallenge.completed == False
    ).first()
    
    if not user_challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="진행 중인 챌린지를 찾을 수 없습니다."
        )
    
    # Update progress
    user_challenge.current_progress = min(
        user_challenge.challenge.target_value,
        user_challenge.current_progress + request.progress_value
    )
    
    # Check if challenge is completed
    if user_challenge.current_progress >= user_challenge.challenge.target_value:
        user_challenge.completed = True
        user_challenge.completed_at = datetime.utcnow()
        
        # TODO: Award badge if associated with challenge
        
        message = f"축하합니다! '{user_challenge.challenge.name}' 챌린지를 완료했습니다! 🎉"
    else:
        progress_percentage = (user_challenge.current_progress / user_challenge.challenge.target_value) * 100
        message = f"진행률: {progress_percentage:.1f}% ({user_challenge.current_progress}/{user_challenge.challenge.target_value})"
    
    db.commit()
    
    return {
        "message": message,
        "completed": user_challenge.completed,
        "current_progress": user_challenge.current_progress,
        "target_value": user_challenge.challenge.target_value
    }

# Initialize default challenges
@router.post("/initialize-default")
async def initialize_default_challenges(db: Session = Depends(get_db)):
    """기본 챌린지 초기화 (관리자용)"""
    
    default_challenges = [
        {
            "name": "일주일 탄소 감축 도전",
            "description": "일주일 동안 탄소 배출량을 20% 줄여보세요!",
            "challenge_type": ChallengeType.CARBON_REDUCTION,
            "target_value": 5,  # 5kg CO2e 감축
            "badge_icon": "🌱",
            "duration_days": 7
        },
        {
            "name": "꾸준한 식사 기록",
            "description": "30일 동안 매일 식사를 기록해보세요!",
            "challenge_type": ChallengeType.MEAL_LOGGING,
            "target_value": 30,  # 30회 식사 기록
            "badge_icon": "📝",
            "duration_days": 30
        },
        {
            "name": "스마트 스왑 마스터",
            "description": "이번 달에 스마트 스왑을 10번 실천해보세요!",
            "challenge_type": ChallengeType.SWAP_ACCEPTANCE,
            "target_value": 10,  # 10번 스왑 수락
            "badge_icon": "🔄",
            "duration_days": 30
        },
        {
            "name": "주간 그린 라이프",
            "description": "일주일 동안 매일 친환경 식사를 실천해보세요!",
            "challenge_type": ChallengeType.WEEKLY_GOAL,
            "target_value": 7,  # 7일 연속
            "badge_icon": "💚",
            "duration_days": 7
        }
    ]
    
    for challenge_data in default_challenges:
        existing = db.query(Challenge).filter(
            Challenge.name == challenge_data["name"]
        ).first()
        
        if not existing:
            challenge = Challenge(**challenge_data)
            db.add(challenge)
    
    db.commit()
    
    return {"message": "기본 챌린지가 초기화되었습니다."} 