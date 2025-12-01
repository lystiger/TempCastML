@echo off

echo Starting backend...
start cmd /k "cd backend && call venv\Scripts\activate && uvicorn main:app --reload"

echo Starting frontend...
start cmd /k "cd frontend && npm install && npm run dev"

echo Both frontend and backend are starting in separate windows.
echo Close the command prompt windows to stop the applications.
