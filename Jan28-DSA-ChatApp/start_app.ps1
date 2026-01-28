# Start Backend
Write-Host "Starting Backend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "cd backend; uvicorn main:app --reload"

# Start Frontend
Write-Host "Starting Frontend..." -ForegroundColor Green
Start-Process powershell -ArgumentList "cd frontend; npm run dev"

Write-Host "Servers started in separate windows." -ForegroundColor Yellow
