@echo off
echo ========================================
echo   Chess Tutor - Stopping Servers
echo ========================================
echo.

echo [1/2] Stopping Backend (port 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo [2/2] Stopping Frontend (port 3000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do (
    taskkill /PID %%a /F >nul 2>&1
)

echo.
echo ========================================
echo   All servers stopped!
echo ========================================
pause
