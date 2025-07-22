# 🌱 Greenflow Life

> **음식을 통한 탄소 발자국 관리와 지속 가능한 식생활 플랫폼**

[![Deploy Status](https://img.shields.io/badge/Deploy-Ready-brightgreen)](https://github.com/your-username/greenflow-life)
[![Frontend](https://img.shields.io/badge/Frontend-React-blue)](https://reactjs.org/)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-blue)](https://postgresql.org/)

## 📖 프로젝트 소개

Greenflow Life는 사용자의 식습관을 통해 탄소 발자국을 계산하고 관리할 수 있는 웹 애플리케이션입니다. 한국 음식 데이터를 기반으로 정확한 탄소 배출량을 계산하고, 개인화된 친환경 식단 추천을 제공합니다.

### ✨ 주요 기능

- 🍽️ **식사 로그 관리**: 음식별 정확한 탄소 발자국 계산
- 📊 **대시보드**: 실시간 통계 및 트렌드 분석
- 🔄 **스마트 스왑**: 친환경 대체 음식 추천
- 🏆 **게이미피케이션**: 배지 시스템 및 챌린지
- 📈 **진행률 추적**: 개인 목표 대비 달성률 모니터링
- 🎯 **개인화**: 식단 선호도 기반 맞춤 추천

## 🖥️ 데모

- **라이브 데모**: [https://greenflow-life.vercel.app](https://greenflow-life.vercel.app)
- **API 문서**: [https://greenflow-api.onrender.com/docs](https://greenflow-api.onrender.com/docs)

## 🛠️ 기술 스택

### Frontend
- **React 18** + TypeScript
- **Tailwind CSS** for styling
- **Framer Motion** for animations
- **React Hook Form** for form management
- **Recharts** for data visualization
- **React Query** for API state management

### Backend
- **FastAPI** (Python)
- **SQLAlchemy** ORM
- **PostgreSQL** database
- **JWT** authentication
- **Pydantic** for data validation
- **Uvicorn** ASGI server

### Deployment
- **Frontend**: Vercel
- **Backend**: Render
- **Database**: Render PostgreSQL

## �� 빠른 시작

### 사전 요구사항
- Node.js 16+
- Python 3.9+
- PostgreSQL (또는 SQLite for development)

### 로컬 개발 환경 설정

#### 1. 리포지토리 클론
```bash
git clone https://github.com/your-username/greenflow-life.git
cd greenflow-life
```

#### 2. 백엔드 설정
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 환경 변수 설정
cp env.production.example .env
# .env 파일을 편집하여 적절한 값 설정

# 데이터베이스 초기화
python -m uvicorn app.main:app --reload
```

#### 3. 프론트엔드 설정
```bash
cd frontend
npm install

# 환경 변수 설정
cp env.production.example .env.local
# .env.local 파일을 편집하여 백엔드 URL 설정

# 개발 서버 시작
npm start
```

#### 4. 접속
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API 문서**: http://localhost:8000/docs

## 📦 배포하기

### 자동 배포
1. **계정 준비**: [GitHub](https://github.com), [Render](https://render.com), [Vercel](https://vercel.com)
2. **상세 가이드**: [`배포_가이드.md`](./배포_가이드.md) 참조
3. **체크리스트**: [`배포_준비_체크리스트.md`](./배포_준비_체크리스트.md) 확인

### 빠른 배포 명령어
```bash
# GitHub에 코드 업로드
git add .
git commit -m "Ready for deployment"
git push origin main

# Render와 Vercel에서 자동 배포됨
```

## 📱 사용 방법

### 1. 회원가입 및 온보딩
- 이름, 식단 선호도, 월간 목표 설정
- 개인화된 대시보드 생성

### 2. 식사 로그 작성
- 음식 이름과 포션 크기 입력
- 실시간 탄소 발자국 계산 확인
- 지속가능성 등급 확인

### 3. 스마트 추천 활용
- 친환경 대체 음식 추천 확인
- 탄소 절약량 비교
- 추천 수락으로 실제 절약 달성

### 4. 진행률 추적
- 주간/월간 통계 확인
- 목표 대비 달성률 모니터링
- 개인화된 인사이트 확인

## 🎯 로드맵

### v1.1 (계획 중)
- [ ] PWA (Progressive Web App) 지원
- [ ] 오프라인 모드
- [ ] 푸시 알림
- [ ] 음식 이미지 인식 (AI)

### v1.2 (계획 중)
- [ ] 소셜 기능 (친구, 그룹 챌린지)
- [ ] 레시피 추천
- [ ] 마트 연동 (장보기 최적화)
- [ ] 탄소 상쇄 프로그램 연결

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 👥 팀

- **Developer**: AI Assistant with Cursor
- **Designer**: Tailwind CSS + Framer Motion
- **Data**: 한국 음식 탄소 발자국 데이터

## 📞 지원

- **Issues**: [GitHub Issues](https://github.com/your-username/greenflow-life/issues)
- **Discussion**: [GitHub Discussions](https://github.com/your-username/greenflow-life/discussions)
- **Email**: support@greenflow.life

---

<div align="center">

**🌱 지속 가능한 미래를 위한 첫 걸음 🌱**

Made with ❤️ for the environment

</div>