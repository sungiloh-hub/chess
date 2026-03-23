@echo off
echo ========================================
echo   Chess Tutor - Starting Servers
echo ========================================
echo.

echo [1/2] Starting Backend (FastAPI)...
cd /d "%~dp0backend"
start "Chess-Backend" cmd /k ".venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000"

echo [2/2] Starting Frontend (Next.js)...
cd /d "%~dp0frontend"
start "Chess-Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo   Servers Starting!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:3000
echo   API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press any key to open the game in browser...
pause >nul
start http://localhost:3000
