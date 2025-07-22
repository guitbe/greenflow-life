"""
한국 음식별 탄소 발자국 데이터베이스
단위: kgCO2eq per serving (1인분 기준)
출처: 국내외 LCA 연구 자료 종합
"""

# 한국 음식별 탄소 발자국 (1인분 기준)
KOREAN_FOOD_CARBON_DB = {
    # 국물 요리 (고탄소)
    "설렁탕": 10.01,
    "갈비탕": 5.05,
    "곰탕": 8.54,
    "갈비찜": 12.3,
    "꼬리곰탕": 9.87,
    "사골국": 7.23,
    "육개장": 4.82,
    
    # 국물 요리 (중간 탄소)
    "닭곰탕": 2.01,
    "삼계탕": 2.45,
    "닭개장": 1.89,
    "추어탕": 1.67,
    "해장국": 2.34,
    "알탕": 1.92,
    
    # 국물 요리 (저탄소)
    "김치찌개": 1.2,
    "된장찌개": 0.8,
    "순두부찌개": 0.6,
    "미역국": 0.3,
    "무국": 0.25,
    "콩나물국": 0.28,
    "북엇국": 0.45,
    "시금치국": 0.22,
    
    # 구이 요리 (고탄소)
    "불고기": 8.5,
    "갈비": 12.3,
    "LA갈비": 11.8,
    "돼지갈비": 7.2,
    "삼겹살": 6.8,
    "목살": 5.9,
    "등심": 9.2,
    "안심": 8.7,
    "한우구이": 15.6,
    
    # 구이 요리 (중간 탄소)
    "닭갈비": 2.1,
    "닭불고기": 1.8,
    "제육볶음": 4.2,
    "오징어볶음": 1.3,
    "낙지볶음": 1.5,
    "생선구이": 1.2,
    "고등어구이": 1.0,
    "삼치구이": 1.1,
    
    # 밥 요리
    "비빔밥": 1.5,
    "김치볶음밥": 2.1,
    "볶음밥": 1.8,
    "오므라이스": 2.3,
    "카레라이스": 2.7,
    "덮밥": 3.2,
    "불고기덮밥": 6.8,
    "치킨마요덮밥": 3.9,
    
    # 면 요리
    "냉면": 1.8,
    "물냉면": 1.6,
    "비빔냉면": 1.9,
    "짜장면": 2.5,
    "짬뽕": 3.2,
    "우동": 1.4,
    "라면": 1.1,
    "잔치국수": 0.9,
    "칼국수": 1.3,
    "수제비": 1.0,
    
    # 한식 반찬류
    "김치": 0.1,
    "깍두기": 0.12,
    "나물반찬": 0.08,
    "콩나물무침": 0.06,
    "시금치나물": 0.05,
    "도라지나물": 0.07,
    "고사리나물": 0.09,
    "버섯볶음": 0.11,
    
    # 찜 요리
    "갈비찜": 12.3,
    "찜닭": 2.8,
    "아귀찜": 1.9,
    "코다리찜": 1.4,
    "돼지족발": 5.6,
    "보쌈": 4.8,
    
    # 전골/전골류
    "부대찌개": 3.4,
    "김치찌개": 1.2,
    "청국장": 0.7,
    "고등어조림": 1.1,
    "갈치조림": 1.3,
    "두부조림": 0.4,
    
    # 해산물 요리
    "회": 2.1,
    "초밥": 1.8,
    "연어회": 2.3,
    "광어회": 1.9,
    "새우": 3.2,
    "게": 2.8,
    "조개찜": 1.6,
    "굴": 0.8,
    
    # 치킨/양식
    "후라이드치킨": 3.1,
    "양념치킨": 3.3,
    "간장치킨": 3.0,
    "파스타": 2.1,
    "피자": 4.5,
    "햄버거": 5.2,
    "스테이크": 18.7,
    
    # 디저트/음료
    "팥빙수": 0.8,
    "아이스크림": 1.2,
    "케이크": 2.1,
    "커피": 0.3,
    "녹차": 0.05,
    "주스": 0.4,
    
    # 간식류
    "김밥": 1.3,
    "토스트": 1.1,
    "샌드위치": 1.8,
    "핫도그": 2.3,
    "떡볶이": 0.9,
    "순대": 2.1,
    "어묵": 0.7,
    "붕어빵": 0.4,
}

# 음식 카테고리별 분류
FOOD_CATEGORIES = {
    "국물요리": ["설렁탕", "갈비탕", "곰탕", "닭곰탕", "김치찌개", "된장찌개", "순두부찌개"],
    "구이요리": ["불고기", "갈비", "삼겹살", "닭갈비", "생선구이"],
    "밥요리": ["비빔밥", "김치볶음밥", "볶음밥", "덮밥"],
    "면요리": ["냉면", "짜장면", "짬뽕", "우동", "라면"],
    "해산물": ["회", "초밥", "새우", "게", "조개찜", "굴"],
    "치킨양식": ["후라이드치킨", "양념치킨", "파스타", "피자", "햄버거"],
    "찜조림": ["갈비찜", "찜닭", "보쌈", "족발"],
    "간식": ["김밥", "토스트", "떡볶이", "순대"],
    "반찬": ["김치", "나물반찬", "콩나물무침"],
    "디저트": ["팥빙수", "아이스크림", "케이크"],
}

def get_food_carbon_footprint(food_name: str, portion_ratio: float = 1.0) -> float:
    """
    음식명으로 탄소 발자국 조회
    
    Args:
        food_name: 음식명
        portion_ratio: 기본 1인분 대비 비율 (예: 0.5 = 반인분, 2.0 = 2인분)
    
    Returns:
        탄소 발자국 (kgCO2eq)
    """
    base_footprint = KOREAN_FOOD_CARBON_DB.get(food_name, 1.0)  # 기본값 1.0kg
    return base_footprint * portion_ratio

def search_similar_foods(query: str) -> list:
    """음식명 검색 시 유사한 음식들 반환"""
    query = query.lower()
    matches = []
    
    for food_name in KOREAN_FOOD_CARBON_DB.keys():
        if query in food_name.lower():
            matches.append({
                "name": food_name,
                "carbon_footprint": KOREAN_FOOD_CARBON_DB[food_name],
                "category": get_food_category(food_name)
            })
    
    # 탄소 발자국 순으로 정렬 (낮은 순)
    return sorted(matches, key=lambda x: x["carbon_footprint"])

def get_food_category(food_name: str) -> str:
    """음식의 카테고리 반환"""
    for category, foods in FOOD_CATEGORIES.items():
        if food_name in foods:
            return category
    return "기타"

def get_foods_by_category(category: str) -> list:
    """카테고리별 음식 목록 반환"""
    return FOOD_CATEGORIES.get(category, [])

def get_low_carbon_alternatives(food_name: str, max_results: int = 3) -> list:
    """특정 음식의 저탄소 대안 추천"""
    if food_name not in KOREAN_FOOD_CARBON_DB:
        return []
    
    original_carbon = KOREAN_FOOD_CARBON_DB[food_name]
    original_category = get_food_category(food_name)
    
    # 같은 카테고리에서 더 낮은 탄소 발자국을 가진 음식들 찾기
    alternatives = []
    category_foods = get_foods_by_category(original_category)
    
    for alt_food in category_foods:
        alt_carbon = KOREAN_FOOD_CARBON_DB[alt_food]
        if alt_carbon < original_carbon:
            carbon_reduction = original_carbon - alt_carbon
            reduction_percentage = (carbon_reduction / original_carbon) * 100
            
            alternatives.append({
                "name": alt_food,
                "carbon_footprint": alt_carbon,
                "carbon_reduction": carbon_reduction,
                "reduction_percentage": reduction_percentage
            })
    
    # 탄소 절약량 순으로 정렬하여 상위 결과 반환
    alternatives.sort(key=lambda x: x["carbon_reduction"], reverse=True)
    return alternatives[:max_results] 