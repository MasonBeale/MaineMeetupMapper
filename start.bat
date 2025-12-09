@echo off
echo Starting MaineMeetupMapper...
echo.

REM Start Flask backend
start "Flask Backend" cmd /k "cd backend && python app.py"

REM Wait a moment for Flask to start
timeout /t 3 /nobreak > nul

REM Start Next.js frontend
start "Next.js Frontend" cmd /k "cd frontend && npm run dev"

REM Wait for Next.js to start
timeout /t 8 /nobreak > nul

REM Open the app in browser
start http://localhost:3001

echo.
echo MaineMeetupMapper is starting!
echo Flask Backend: http://127.0.0.1:5000
echo Next.js Frontend: http://localhost:3001
echo.
echo Press any key to exit this window (servers will keep running)
pause > nul