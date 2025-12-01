#!/bin/bash

echo "Starting backend..."
# Navigate to backend, activate venv, and run uvicorn in the background
(cd .. && cd backend && source venv/bin/activate && cd .. && uvicorn backend.main:app --reload) &
BACKEND_PID=$! # Store the PID of the background process

echo "Starting frontend..."
# Navigate to frontend, install dependencies, and run dev server in the background
(cd .. && cd frontend && npm install && npm run dev) &
FRONTEND_PID=$! # Store the PID of the background process

echo "Both frontend and backend are starting in the background."
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "To stop them, use 'kill $BACKEND_PID' and 'kill $FRONTEND_PID' or 'killall uvicorn' and 'killall node'."

wait $BACKEND_PID
wait $FRONTEND_PID
