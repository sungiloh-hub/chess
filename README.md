# FastAPI + Next.js 웹 서비스

FastAPI 백엔드와 Next.js 프론트엔드로 구성된 풀스택 웹 서비스 템플릿입니다.

## 📁 프로젝트 구조

```
fastapi_nextjs/
├── backend/                 # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py         # FastAPI 앱 진입점
│   │   ├── api/routes/     # API 라우터
│   │   ├── core/           # 설정 관리
│   │   └── models/         # 데이터 모델
│   └── requirements.txt
├── frontend/               # Next.js 프론트엔드
│   ├── app/                # App Router 페이지
│   ├── lib/                # 유틸리티 함수
│   └── package.json
└── README.md
```

## 🚀 시작하기

### 사전 요구사항

- Python 3.10+
- Node.js 18+

### 백엔드 실행

```bash
cd backend

# 가상환경 생성 (선택사항)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# 의존성 설치
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

백엔드 API 문서: http://localhost:8000/docs

### 프론트엔드 실행

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```

프론트엔드: http://localhost:3000

## 📚 API 엔드포인트

| Method | Endpoint | 설명 |
|--------|----------|------|
| GET | `/` | 앱 정보 |
| GET | `/api/health` | 헬스체크 |
| GET | `/api/health/ping` | Ping 테스트 |

## 🔧 환경 변수

### 백엔드 (`backend/.env`)

```env
DEBUG=true
FRONTEND_URL=http://localhost:3000
```

### 프론트엔드 (`frontend/.env.local`)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 개발 가이드

### 새 API 엔드포인트 추가

1. `backend/app/api/routes/`에 새 라우터 파일 생성
2. `backend/app/main.py`에 라우터 등록

### 새 페이지 추가

1. `frontend/app/`에 새 폴더/`page.tsx` 생성
2. Next.js App Router 규칙에 따라 자동 라우팅
