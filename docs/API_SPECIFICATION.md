# Greenflow Life API 명세서

## 🔗 기본 정보
- **Base URL**: `https://greenflow-api.render.com/api`
- **Authentication**: JWT Bearer Token
- **Content-Type**: `application/json`

## 🔐 인증 (Authentication)

### 1. 사용자 등록
**Endpoint**: `POST /auth/register`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123",
  "name": "홍길동",
  "dietary_preference": "omnivore"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 400: 이미 등록된 이메일
- 422: 입력 데이터 유효성 검사 실패

### 2. 사용자 로그인
**Endpoint**: `POST /auth/login`

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Response** (200 OK):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses**:
- 401: 이메일 또는 비밀번호 오류

### 3. 현재 사용자 정보 조회
**Endpoint**: `GET /auth/me`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "홍길동",
  "dietary_preference": "omnivore",
  "target_carbon_reduction": 20.0
}
```

## 🍽️ 식사 기록 (Meals)

### 1. 식사 기록 추가
**Endpoint**: `POST /meals/`
**Headers**: `Authorization: Bearer {token}`

**Request Body**:
```json
{
  "food_name": "소고기 불고기",
  "portion_size": 200.0,
  "meal_type": "dinner",
  "image_url": "https://example.com/image.jpg"
}
```

**Response** (200 OK):
```json
{
  "id": 1,
  "food_name": "소고기 불고기",
  "portion_size": 200.0,
  "meal_type": "dinner",
  "carbon_footprint": 5.0,
  "image_url": "https://example.com/image.jpg",
  "logged_at": "2024-01-15T18:30:00"
}
```

### 2. 식사 기록 조회
**Endpoint**: `GET /meals/?skip=0&limit=50`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "food_name": "소고기 불고기",
    "portion_size": 200.0,
    "meal_type": "dinner",
    "carbon_footprint": 5.0,
    "image_url": "https://example.com/image.jpg",
    "logged_at": "2024-01-15T18:30:00"
  }
]
```

### 3. 특정 식사 기록 조회
**Endpoint**: `GET /meals/{meal_id}`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "id": 1,
  "food_name": "소고기 불고기",
  "portion_size": 200.0,
  "meal_type": "dinner",
  "carbon_footprint": 5.0,
  "image_url": "https://example.com/image.jpg",
  "logged_at": "2024-01-15T18:30:00"
}
```

## 🌱 탄소 발자국 계산 (Footprint)

### 1. 탄소 발자국 계산
**Endpoint**: `POST /footprint/calculate`
**Headers**: `Authorization: Bearer {token}`

**Request Body**:
```json
{
  "food_name": "소고기",
  "portion_size": 200.0
}
```

**Response** (200 OK):
```json
{
  "food_name": "소고기",
  "portion_size": 200.0,
  "carbon_footprint": 5.0,
  "category": "육류",
  "sustainability_rating": "LOW"
}
```

**지속가능성 등급**:
- `HIGH`: 탄소 발자국이 낮음 (< 0.5kg CO₂e)
- `MEDIUM`: 보통 수준 (0.5-1.5kg CO₂e)
- `LOW`: 탄소 발자국이 높음 (> 1.5kg CO₂e)

### 2. 일별 탄소 발자국 요약
**Endpoint**: `GET /footprint/daily-summary?days=7`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
[
  {
    "date": "2024-01-15",
    "total_carbon": 12.5,
    "meal_count": 3,
    "top_contributor": "소고기 불고기"
  }
]
```

## 🔄 스마트 스왑 추천 (Swaps)

### 1. 식사 대체 추천 조회
**Endpoint**: `GET /swaps/{meal_id}`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "meal_log_id": 1,
  "recommendations": [
    {
      "original_food": "소고기",
      "recommended_food": "닭고기",
      "carbon_reduction": 1.9,
      "carbon_reduction_percentage": 76.0,
      "recommendation_message": "소고기 대신 닭고기는 어떠세요? 탄소 배출량을 76% 줄일 수 있어요!",
      "category": "육류"
    }
  ]
}
```

### 2. 스왑 추천 수락/거절
**Endpoint**: `POST /swaps/accept`
**Headers**: `Authorization: Bearer {token}`

**Request Body**:
```json
{
  "swap_id": 1,
  "accepted": true
}
```

**Response** (200 OK):
```json
{
  "message": "추천이 업데이트되었습니다.",
  "accepted": true
}
```

## 📊 대시보드 (Dashboard)

### 1. 대시보드 데이터 조회
**Endpoint**: `GET /dashboard/`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
{
  "stats": {
    "total_carbon_this_week": 25.5,
    "carbon_reduction_achieved": 3.2,
    "target_progress_percentage": 64.0,
    "meals_logged_this_week": 15,
    "swaps_accepted": 5,
    "active_challenges": 2,
    "completed_challenges": 1
  },
  "carbon_trends": [
    {
      "date": "2024-01-15",
      "carbon_amount": 8.5,
      "meal_count": 3
    }
  ],
  "top_contributors": [
    {
      "food_name": "소고기 불고기",
      "total_carbon": 15.0,
      "frequency": 3
    }
  ],
  "insights": [
    {
      "type": "achievement",
      "title": "훌륭해요! 🎉",
      "message": "이번 달에 5개의 스마트 스왑을 실천하여 3.2kg의 탄소를 절약했어요!",
      "icon": "🌱",
      "action_text": "더 많은 스왑 보기"
    }
  ]
}
```

## 🏆 챌린지 (Challenges)

### 1. 참여 가능한 챌린지 조회
**Endpoint**: `GET /challenges/available`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "일주일 탄소 감축 도전",
    "description": "일주일 동안 탄소 배출량을 20% 줄여보세요!",
    "challenge_type": "carbon_reduction",
    "target_value": 5,
    "badge_icon": "🌱",
    "duration_days": 7,
    "is_active": true
  }
]
```

### 2. 내 챌린지 조회
**Endpoint**: `GET /challenges/my-challenges`
**Headers**: `Authorization: Bearer {token}`

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "challenge": {
      "id": 1,
      "name": "일주일 탄소 감축 도전",
      "description": "일주일 동안 탄소 배출량을 20% 줄여보세요!",
      "challenge_type": "carbon_reduction",
      "target_value": 5,
      "badge_icon": "🌱",
      "duration_days": 7,
      "is_active": true
    },
    "current_progress": 3,
    "completed": false,
    "progress_percentage": 60.0,
    "started_at": "2024-01-10T00:00:00",
    "completed_at": null,
    "days_remaining": 3
  }
]
```

### 3. 챌린지 참여
**Endpoint**: `POST /challenges/join`
**Headers**: `Authorization: Bearer {token}`

**Request Body**:
```json
{
  "challenge_id": 1
}
```

**Response** (200 OK):
```json
{
  "message": "챌린지에 성공적으로 참여했습니다!",
  "challenge_name": "일주일 탄소 감축 도전"
}
```

### 4. 챌린지 진행 상황 업데이트
**Endpoint**: `PATCH /challenges/update-progress`
**Headers**: `Authorization: Bearer {token}`

**Request Body**:
```json
{
  "challenge_id": 1,
  "progress_value": 1
}
```

**Response** (200 OK):
```json
{
  "message": "진행률: 80.0% (4/5)",
  "completed": false,
  "current_progress": 4,
  "target_value": 5
}
```

**완료 시 Response**:
```json
{
  "message": "축하합니다! '일주일 탄소 감축 도전' 챌린지를 완료했습니다! 🎉",
  "completed": true,
  "current_progress": 5,
  "target_value": 5
}
```

## ❌ 공통 에러 응답

### 401 Unauthorized
```json
{
  "detail": "토큰이 유효하지 않습니다."
}
```

### 403 Forbidden
```json
{
  "detail": "접근 권한이 없습니다."
}
```

### 404 Not Found
```json
{
  "detail": "요청한 리소스를 찾을 수 없습니다."
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "food_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "서버 내부 오류가 발생했습니다."
}
```

## 📝 사용 예시

### 전체 플로우 예시
```javascript
// 1. 로그인
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password123'
  })
});
const { access_token } = await loginResponse.json();

// 2. 식사 기록
const mealResponse = await fetch('/api/meals/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${access_token}`
  },
  body: JSON.stringify({
    food_name: '소고기 불고기',
    portion_size: 200.0,
    meal_type: 'dinner'
  })
});
const meal = await mealResponse.json();

// 3. 스왑 추천 조회
const swapResponse = await fetch(`/api/swaps/${meal.id}`, {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const swaps = await swapResponse.json();

// 4. 대시보드 조회
const dashboardResponse = await fetch('/api/dashboard/', {
  headers: { 'Authorization': `Bearer ${access_token}` }
});
const dashboard = await dashboardResponse.json();
```

## 🔧 Rate Limiting
- 일반 API: 1000 requests/hour per user
- 인증 API: 10 requests/minute per IP
- 파일 업로드: 50 requests/hour per user 