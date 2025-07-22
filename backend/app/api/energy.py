from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.core.database import get_db
from app.api.auth import get_current_user
from app.models.user import User
from app.models.activity_log import ActivityLog, ActivityType
from app.data.korean_emission_factors import (
    get_electricity_co2, 
    get_gas_co2, 
    get_transport_co2,
    get_fuel_co2
)

router = APIRouter()

class EnergyCalculationRequest(BaseModel):
    electricity_kwh: Optional[float] = None
    electricity_bill_amount: Optional[float] = None  # 전기요금(원)
    gas_m3: Optional[float] = None
    gas_bill_amount: Optional[float] = None  # 가스요금(원)

class EnergyCalculationResponse(BaseModel):
    electricity_footprint: float
    gas_footprint: float
    total_energy_footprint: float
    electricity_kwh_used: Optional[float]
    gas_m3_used: Optional[float]

class TransportCalculationRequest(BaseModel):
    transport_type: str  # car_gasoline, bus_city, subway, etc.
    distance_km: Optional[float] = None
    fuel_liters: Optional[float] = None
    fuel_cost: Optional[float] = None

class TransportCalculationResponse(BaseModel):
    transport_footprint: float
    transport_type: str
    distance_km: Optional[float]
    fuel_efficiency_info: Optional[str]

@router.post("/energy/calculate", response_model=EnergyCalculationResponse)
async def calculate_energy_footprint(
    request: EnergyCalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """가정 에너지 사용량 기반 탄소 발자국 계산"""
    
    electricity_footprint = 0.0
    gas_footprint = 0.0
    electricity_kwh_used = None
    gas_m3_used = None
    
    # 전기 사용량 계산
    if request.electricity_kwh:
        electricity_kwh_used = request.electricity_kwh
        electricity_footprint = get_electricity_co2(request.electricity_kwh)
    elif request.electricity_bill_amount:
        # 전기요금으로부터 사용량 추정 (평균 전기요금 120원/kWh 가정)
        estimated_kwh = request.electricity_bill_amount / 120.0
        electricity_kwh_used = estimated_kwh
        electricity_footprint = get_electricity_co2(estimated_kwh)
    
    # 가스 사용량 계산
    if request.gas_m3:
        gas_m3_used = request.gas_m3
        gas_footprint = get_gas_co2(request.gas_m3)
    elif request.gas_bill_amount:
        # 가스요금으로부터 사용량 추정 (평균 가스요금 800원/m³ 가정)
        estimated_m3 = request.gas_bill_amount / 800.0
        gas_m3_used = estimated_m3
        gas_footprint = get_gas_co2(estimated_m3)
    
    total_footprint = electricity_footprint + gas_footprint
    
    # ActivityLog에 기록
    if total_footprint > 0:
        activity_log = ActivityLog(
            user_id=current_user.id,
            activity_type=ActivityType.ENERGY,
            energy_usage=electricity_kwh_used or 0,
            carbon_footprint=total_footprint
        )
        db.add(activity_log)
        db.commit()
    
    return EnergyCalculationResponse(
        electricity_footprint=round(electricity_footprint, 3),
        gas_footprint=round(gas_footprint, 3),
        total_energy_footprint=round(total_footprint, 3),
        electricity_kwh_used=electricity_kwh_used,
        gas_m3_used=gas_m3_used
    )

@router.post("/transport/calculate", response_model=TransportCalculationResponse)
async def calculate_transport_footprint(
    request: TransportCalculationRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """교통수단 이용 기반 탄소 발자국 계산"""
    
    transport_footprint = 0.0
    distance_km = request.distance_km
    fuel_efficiency_info = None
    
    if request.distance_km:
        # 거리 기반 계산
        transport_footprint = get_transport_co2(request.transport_type, request.distance_km)
    elif request.fuel_liters:
        # 연료 사용량 기반 계산 (자가용의 경우)
        if "car" in request.transport_type:
            fuel_type = "gasoline" if "gasoline" in request.transport_type else "diesel"
            transport_footprint = get_fuel_co2(fuel_type, request.fuel_liters)
            
            # 연비 정보 제공
            if request.transport_type == "car_gasoline":
                estimated_distance = request.fuel_liters * 12  # 평균 연비 12km/L
                fuel_efficiency_info = f"추정 주행거리: {estimated_distance:.1f}km (연비 12km/L 기준)"
                distance_km = estimated_distance
            elif request.transport_type == "car_diesel":
                estimated_distance = request.fuel_liters * 15  # 평균 연비 15km/L
                fuel_efficiency_info = f"추정 주행거리: {estimated_distance:.1f}km (연비 15km/L 기준)"
                distance_km = estimated_distance
    
    # ActivityLog에 기록
    if transport_footprint > 0:
        activity_log = ActivityLog(
            user_id=current_user.id,
            activity_type=ActivityType.TRANSPORT,
            transport_mode=getattr(ActivityType, request.transport_type.upper(), None),
            distance_km=distance_km,
            carbon_footprint=transport_footprint
        )
        db.add(activity_log)
        db.commit()
    
    return TransportCalculationResponse(
        transport_footprint=round(transport_footprint, 3),
        transport_type=request.transport_type,
        distance_km=distance_km,
        fuel_efficiency_info=fuel_efficiency_info
    )

@router.get("/transport/types")
async def get_transport_types():
    """사용 가능한 교통수단 목록 반환"""
    
    transport_types = {
        "개인교통": {
            "car_gasoline": "승용차 (휘발유)",
            "car_diesel": "승용차 (경유)", 
            "car_lpg": "승용차 (LPG)",
            "electric_car": "전기차",
            "motorcycle": "오토바이"
        },
        "대중교통": {
            "bus_city": "시내버스",
            "bus_express": "고속버스",
            "subway": "지하철",
            "train_ktx": "KTX",
            "train_regular": "일반열차"
        },
        "항공": {
            "airplane_domestic": "국내선",
            "airplane_international": "국제선"
        },
        "친환경": {
            "bicycle": "자전거",
            "walking": "도보"
        }
    }
    
    return transport_types

@router.get("/energy/monthly-average")
async def get_monthly_energy_average(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자의 월평균 에너지 사용량 및 탄소 발자국"""
    
    from sqlalchemy import func, extract
    from datetime import datetime, timedelta
    
    # 최근 6개월 데이터 조회
    six_months_ago = datetime.now() - timedelta(days=180)
    
    monthly_data = db.query(
        extract('year', ActivityLog.logged_at).label('year'),
        extract('month', ActivityLog.logged_at).label('month'),
        func.sum(ActivityLog.carbon_footprint).label('total_carbon'),
        func.sum(ActivityLog.energy_usage).label('total_energy')
    ).filter(
        ActivityLog.user_id == current_user.id,
        ActivityLog.activity_type == ActivityType.ENERGY,
        ActivityLog.logged_at >= six_months_ago
    ).group_by(
        extract('year', ActivityLog.logged_at),
        extract('month', ActivityLog.logged_at)
    ).all()
    
    if not monthly_data:
        return {
            "average_monthly_carbon": 0.0,
            "average_monthly_energy": 0.0,
            "data_points": 0,
            "recommendation": "아직 에너지 사용 데이터가 없습니다. 전기/가스 사용량을 기록해보세요!"
        }
    
    avg_carbon = sum(data.total_carbon for data in monthly_data) / len(monthly_data)
    avg_energy = sum(data.total_energy or 0 for data in monthly_data) / len(monthly_data)
    
    # 권장사항 생성
    if avg_carbon > 150:  # 월 150kg 이상
        recommendation = "평균보다 높은 에너지 사용량입니다. LED 전구 교체나 절전형 가전제품 사용을 고려해보세요."
    elif avg_carbon > 100:
        recommendation = "적정 수준의 에너지 사용량입니다. 조금 더 절약해보면 어떨까요?"
    else:
        recommendation = "훌륭한 에너지 절약 실천입니다! 계속 유지해주세요."
    
    return {
        "average_monthly_carbon": round(avg_carbon, 2),
        "average_monthly_energy": round(avg_energy, 2),
        "data_points": len(monthly_data),
        "recommendation": recommendation
    } 