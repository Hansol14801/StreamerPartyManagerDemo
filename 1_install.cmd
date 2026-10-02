@echo off
chcp 65001 >nul
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  echo Python이 없습니다. Python 3.12 설치를 시도합니다...
  where winget >nul 2>nul
  if errorlevel 1 (
    echo winget을 찾을 수 없습니다. Python 3.10 이상을 설치해주세요.
    pause
    exit /b 1
  )
  winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements
)
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
echo.
echo Demo 설치 완료. 2_start_demo.cmd를 실행하세요.
pause
