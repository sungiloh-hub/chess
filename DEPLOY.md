# 🚀 Chess Tutor 배포 가이드

PC 없이 폰에서만 사용하기 위한 무료 클라우드 배포 가이드입니다.

## 전체 구조

```
[가족 폰 브라우저] ──인터넷──▶ Vercel (프론트엔드, 무료)
                                    │
                                    ▼
                              Render (백엔드, 무료)
```

---

## 사전 준비

1. **GitHub 계정** 만들기: https://github.com
2. **Render 계정** 만들기: https://render.com (GitHub으로 로그인)
3. **Vercel 계정** 만들기: https://vercel.com (GitHub으로 로그인)

---

## Step 1: GitHub에 코드 올리기

### 1-1. Git 초기화 (PC에서 한번만)

```powershell
cd C:\Users\Julian\Desktop\fastapi_nextjs
git init
git add .
git commit -m "Chess Tutor initial commit"
```

### 1-2. GitHub에 저장소 만들기

1. https://github.com/new 접속
2. Repository name: `chess-tutor`
3. Private 선택 (가족만 사용하므로)
4. Create repository 클릭

### 1-3. 코드 푸시

```powershell
git remote add origin https://github.com/YOUR_USERNAME/chess-tutor.git
git branch -M main
git push -u origin main
```

---

## Step 2: 백엔드 배포 (Render.com)

### 2-1. Render에서 새 서비스 생성

1. https://dashboard.render.com 접속
2. **New +** → **Web Service** 클릭
3. GitHub 저장소 연결 → `chess-tutor` 선택

### 2-2. 설정

| 항목 | 값 |
|------|-----|
| **Name** | `chess-tutor-api` |
| **Root Directory** | `backend` |
| **Runtime** | `Python` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### 2-3. 환경 변수 추가

| Key | Value |
|-----|-------|
| `DEBUG` | `false` |
| `FRONTEND_URL` | (Step 3에서 Vercel URL을 받은 후 추가) |

### 2-4. Deploy 클릭!

배포가 완료되면 URL을 받습니다 (예: `https://chess-tutor-api.onrender.com`)

> ⚡ 이 URL을 메모해두세요! 프론트엔드 설정에 필요합니다.

---

## Step 3: 프론트엔드 배포 (Vercel)

### 3-1. Vercel에서 새 프로젝트 생성

1. https://vercel.com/new 접속
2. GitHub 저장소 → `chess-tutor` 선택
3. **Import** 클릭

### 3-2. 설정

| 항목 | 값 |
|------|-----|
| **Framework Preset** | `Next.js` (자동 감지) |
| **Root Directory** | `frontend` |

### 3-3. 환경 변수 추가

| Key | Value |
|-----|-------|
| `NEXT_PUBLIC_API_URL` | `https://chess-tutor-api.onrender.com` (Step 2에서 받은 URL) |

### 3-4. Deploy 클릭!

배포 완료 후 URL을 받습니다 (예: `https://chess-tutor.vercel.app`)

---

## Step 4: Render에 프론트엔드 URL 추가

1. Render 대시보드 → `chess-tutor-api` → Environment
2. 환경 변수 추가:
   - `FRONTEND_URL` = `https://chess-tutor.vercel.app` (Step 3에서 받은 URL)
3. Save & Redeploy

---

## Step 5: 폰에서 접속! 🎉

1. 폰 브라우저(Chrome)에서 Vercel URL 접속:
   ```
   https://chess-tutor.vercel.app
   ```

2. 홈 화면에 추가 (앱처럼 사용):
   - Chrome → 메뉴(⋮) → "홈 화면에 추가"
   - 앱 이름: "Chess Tutor"
   - 추가 클릭!

3. 가족들에게 URL 공유하면 끝!

---

## ⚠️ 참고사항

### Render 무료 플랜 제한
- 15분간 요청이 없으면 서버가 **절전 모드**로 전환됩니다
- 다시 접속하면 **약 30초~1분** 후에 깨어납니다
- 첫 접속만 느리고, 이후에는 정상 속도입니다

### 업데이트 방법
코드를 수정하고 GitHub에 push하면 **자동으로 재배포**됩니다:
```powershell
git add .
git commit -m "업데이트 내용"
git push
```

---

## 요약

| 서비스 | 용도 | 비용 | URL 예시 |
|--------|------|------|----------|
| **GitHub** | 코드 저장 | 무료 | github.com/username/chess-tutor |
| **Render** | 백엔드 API | 무료 | chess-tutor-api.onrender.com |
| **Vercel** | 프론트엔드 | 무료 | chess-tutor.vercel.app |
