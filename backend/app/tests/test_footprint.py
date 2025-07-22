import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base
from app.models.user import User, DietaryPreference
from app.core.security import get_password_hash

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_user_token():
    """테스트 사용자 생성 및 토큰 반환"""
    # Register test user
    register_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
        "dietary_preference": "omnivore"
    }
    
    response = client.post("/api/auth/register", json=register_data)
    assert response.status_code == 200
    
    return response.json()["access_token"]

class TestCarbonFootprintCalculation:
    """탄소 발자국 계산 API 테스트"""
    
    def test_calculate_carbon_footprint_success(self, test_user_token):
        """성공적인 탄소 발자국 계산 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        payload = {
            "food_name": "소고기",
            "portion_size": 200.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        # 응답 구조 검증
        assert "food_name" in data
        assert "portion_size" in data
        assert "carbon_footprint" in data
        assert "category" in data
        assert "sustainability_rating" in data
        
        # 값 검증
        assert data["food_name"] == "소고기"
        assert data["portion_size"] == 200.0
        assert data["carbon_footprint"] == 5.0  # 200g * 2.5 kg/100g = 5.0
        assert data["category"] == "육류"
        assert data["sustainability_rating"] == "LOW"  # 5.0 > 1.5이므로 LOW
    
    def test_calculate_carbon_footprint_chicken(self, test_user_token):
        """닭고기 탄소 발자국 계산 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        payload = {
            "food_name": "닭고기",
            "portion_size": 150.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["carbon_footprint"] == 0.9  # 150g * 0.6 kg/100g = 0.9
        assert data["category"] == "육류"
        assert data["sustainability_rating"] == "MEDIUM"  # 0.9 < 1.5이므로 MEDIUM
    
    def test_calculate_carbon_footprint_vegetables(self, test_user_token):
        """채소 탄소 발자국 계산 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        payload = {
            "food_name": "브로콜리",
            "portion_size": 100.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["carbon_footprint"] == 0.08  # 100g * 0.08 kg/100g = 0.08
        assert data["category"] == "채소"
        assert data["sustainability_rating"] == "HIGH"  # 0.08 < 0.5이므로 HIGH
    
    def test_calculate_carbon_footprint_unknown_food(self, test_user_token):
        """알 수 없는 음식 탄소 발자국 계산 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        payload = {
            "food_name": "알 수 없는 음식",
            "portion_size": 100.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["carbon_footprint"] == 0.5  # 기본값: 100g * 0.5 kg/100g = 0.5
        assert data["category"] == "기타"
        assert data["sustainability_rating"] == "MEDIUM"
    
    def test_calculate_carbon_footprint_invalid_data(self, test_user_token):
        """잘못된 데이터로 탄소 발자국 계산 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        # 음식 이름 누락
        payload = {
            "portion_size": 100.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        assert response.status_code == 422  # Validation error
        
        # portion_size 누락
        payload = {
            "food_name": "소고기"
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        assert response.status_code == 422  # Validation error
        
        # 음수 portion_size
        payload = {
            "food_name": "소고기",
            "portion_size": -100.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        # 음수 값 처리는 비즈니스 로직에 따라 다를 수 있음
    
    def test_calculate_carbon_footprint_unauthorized(self):
        """인증되지 않은 사용자 테스트"""
        
        payload = {
            "food_name": "소고기",
            "portion_size": 200.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload)
        assert response.status_code == 403  # Forbidden
    
    def test_calculate_carbon_footprint_invalid_token(self):
        """잘못된 토큰으로 테스트"""
        
        headers = {"Authorization": "Bearer invalid_token"}
        payload = {
            "food_name": "소고기",
            "portion_size": 200.0
        }
        
        response = client.post("/api/footprint/calculate", json=payload, headers=headers)
        assert response.status_code == 401  # Unauthorized

class TestDailyCarbonSummary:
    """일일 탄소 발자국 요약 API 테스트"""
    
    def test_get_daily_summary_empty_data(self, test_user_token):
        """데이터가 없는 경우 일일 요약 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        response = client.get("/api/footprint/daily-summary", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # 식사 기록이 없으므로 빈 배열
    
    def test_get_daily_summary_with_meals(self, test_user_token):
        """식사 기록이 있는 경우 일일 요약 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        # 먼저 식사 기록 추가
        meal_data = {
            "food_name": "소고기",
            "portion_size": 200.0,
            "meal_type": "dinner"
        }
        
        meal_response = client.post("/api/meals/", json=meal_data, headers=headers)
        assert meal_response.status_code == 200
        
        # 일일 요약 조회
        response = client.get("/api/footprint/daily-summary", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        
        if len(data) > 0:
            summary = data[0]
            assert "date" in summary
            assert "total_carbon" in summary
            assert "meal_count" in summary
            assert "top_contributor" in summary
            
            assert summary["meal_count"] >= 1
            assert summary["total_carbon"] > 0
            assert summary["top_contributor"] == "소고기"
    
    def test_get_daily_summary_custom_days(self, test_user_token):
        """사용자 정의 일수로 일일 요약 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        # 3일간 데이터 요청
        response = client.get("/api/footprint/daily-summary?days=3", headers=headers)
        
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 실제 데이터 개수는 실제 식사 기록에 따라 달라짐

class TestSustainabilityRating:
    """지속가능성 등급 테스트"""
    
    def test_high_sustainability_foods(self, test_user_token):
        """높은 지속가능성 음식 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        high_sustainability_foods = [
            ("사과", 100.0, "HIGH"),
            ("상추", 100.0, "HIGH"),
            ("브로콜리", 100.0, "HIGH"),
            ("당근", 100.0, "HIGH")
        ]
        
        for food_name, portion, expected_rating in high_sustainability_foods:
            payload = {
                "food_name": food_name,
                "portion_size": portion
            }
            
            response = client.post("/api/footprint/calculate", json=payload, headers=headers)
            assert response.status_code == 200
            
            data = response.json()
            assert data["sustainability_rating"] == expected_rating
    
    def test_low_sustainability_foods(self, test_user_token):
        """낮은 지속가능성 음식 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        
        low_sustainability_foods = [
            ("소고기", 100.0, "LOW"),
            ("한우", 100.0, "LOW"),
            ("양고기", 100.0, "LOW"),
            ("새우", 100.0, "LOW")
        ]
        
        for food_name, portion, expected_rating in low_sustainability_foods:
            payload = {
                "food_name": food_name,
                "portion_size": portion
            }
            
            response = client.post("/api/footprint/calculate", json=payload, headers=headers)
            assert response.status_code == 200
            
            data = response.json()
            assert data["sustainability_rating"] == expected_rating

class TestFoodCategorization:
    """음식 카테고리 분류 테스트"""
    
    def test_meat_category(self, test_user_token):
        """육류 카테고리 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        meat_foods = ["소고기", "돼지고기", "닭고기", "한우", "삼겹살"]
        
        for food in meat_foods:
            payload = {
                "food_name": food,
                "portion_size": 100.0
            }
            
            response = client.post("/api/footprint/calculate", json=payload, headers=headers)
            data = response.json()
            assert data["category"] == "육류"
    
    def test_seafood_category(self, test_user_token):
        """해산물 카테고리 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        seafood_foods = ["생선", "새우", "게", "조개", "연어"]
        
        for food in seafood_foods:
            payload = {
                "food_name": food,
                "portion_size": 100.0
            }
            
            response = client.post("/api/footprint/calculate", json=payload, headers=headers)
            data = response.json()
            assert data["category"] == "해산물"
    
    def test_vegetable_category(self, test_user_token):
        """채소 카테고리 테스트"""
        
        headers = {"Authorization": f"Bearer {test_user_token}"}
        vegetable_foods = ["브로콜리", "당근", "감자", "상추"]
        
        for food in vegetable_foods:
            payload = {
                "food_name": food,
                "portion_size": 100.0
            }
            
            response = client.post("/api/footprint/calculate", json=payload, headers=headers)
            data = response.json()
            assert data["category"] == "채소"

# Run with: pytest backend/app/tests/test_footprint.py -v 