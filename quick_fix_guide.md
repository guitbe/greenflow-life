# Python 3.13 호환 모드로 전환하기

## 1. 패키지 업그레이드
```bash
cp backup_requirements_python313.txt backend/requirements.txt
git add backend/requirements.txt
git commit -m "Upgrade to Python 3.13 compatible packages"
git push origin main
```

## 2. 코드 수정이 필요할 수 있는 부분
- Pydantic v1 → v2 마이그레이션
- FastAPI 최신 버전 API 변경사항

## 3. 주요 변경사항
- pydantic 1.10.12 → 2.9.2 (Python 3.13 호환)
- fastapi 0.100.1 → 0.115.0 (최신 안정 버전)
- uvicorn 0.23.2 → 0.32.0 