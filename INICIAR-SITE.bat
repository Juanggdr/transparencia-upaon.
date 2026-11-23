@echo off
cd /d "%~dp0"
echo Abrindo Transparencia Upaon Acu em http://localhost:8080
start "" http://localhost:8080
python -m http.server 8080
if errorlevel 1 py -m http.server 8080
pause
