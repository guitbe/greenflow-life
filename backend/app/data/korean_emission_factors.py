"""
한국 온실가스 배출계수 데이터
출처: 2024년 승인 국가 온실가스 배출 계수 (환경부)
"""

# 전력 배출계수 (tCO2eq/MWh -> kgCO2eq/kWh로 변환)
ELECTRICITY_FACTOR_KG_PER_KWH = 0.4541  # 2024년 기준

# 도시가스 배출계수 (kgCO2eq/m³)
CITY_GAS_FACTOR_KG_PER_M3 = 2.176

# 교통수단별 배출계수 (kgCO2eq/km)
TRANSPORT_FACTORS = {
    # 개인 교통수단
    "car_gasoline": 0.2157,      # 휘발유 승용차
    "car_diesel": 0.1943,        # 경유 승용차
    "car_lpg": 0.1847,          # LPG 승용차
    "motorcycle": 0.0988,        # 오토바이
    
    # 대중교통
    "bus_city": 0.0648,         # 시내버스
    "bus_express": 0.0432,      # 고속버스
    "subway": 0.0288,           # 지하철
    "train_ktx": 0.0156,        # KTX
    "train_regular": 0.0324,    # 일반열차
    
    # 항공
    "airplane_domestic": 0.1576,  # 국내선
    "airplane_international": 0.1899,  # 국제선
    
    # 친환경 교통수단
    "bicycle": 0.0,             # 자전거
    "walking": 0.0,             # 도보
    "electric_car": 0.0541,     # 전기차 (전력 배출계수 적용)
}

# 연료별 배출계수 (kgCO2eq/L)
FUEL_FACTORS = {
    "gasoline": 2.27,           # 휘발유
    "diesel": 2.64,             # 경유
    "lpg": 1.68,               # LPG
    "kerosene": 2.46,          # 등유
}

# 기타 에너지원 배출계수
OTHER_ENERGY_FACTORS = {
    "heating_oil_kg_per_l": 2.68,      # 난방유
    "propane_kg_per_kg": 2.93,         # 프로판
    "butane_kg_per_kg": 2.93,          # 부탄
}

def get_electricity_co2(kwh: float) -> float:
    """전력 사용량(kWh)을 CO2 배출량(kg)으로 변환"""
    return kwh * ELECTRICITY_FACTOR_KG_PER_KWH

def get_gas_co2(m3: float) -> float:
    """도시가스 사용량(m³)을 CO2 배출량(kg)으로 변환"""
    return m3 * CITY_GAS_FACTOR_KG_PER_M3

def get_transport_co2(transport_type: str, distance_km: float) -> float:
    """교통수단별 이동거리(km)를 CO2 배출량(kg)으로 변환"""
    factor = TRANSPORT_FACTORS.get(transport_type, 0.0)
    return distance_km * factor

def get_fuel_co2(fuel_type: str, liters: float) -> float:
    """연료 사용량(L)을 CO2 배출량(kg)으로 변환"""
    factor = FUEL_FACTORS.get(fuel_type, 0.0)
    return liters * factor 