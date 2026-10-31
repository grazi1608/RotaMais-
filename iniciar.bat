@echo off
cd /d "%~dp0"
echo ==========================================
echo   RotaMais - iniciando
echo ==========================================
echo.
echo [1/3] Instalando dependencias (requirements.txt)...
python -m pip install -r requirements.txt
if errorlevel 1 (
  echo.
  echo ERRO: nao foi possivel instalar as dependencias.
  echo Verifique se o Python esta instalado e adicionado ao PATH.
  pause
  exit /b 1
)
echo.
echo [2/3] Iniciando a API (backend) em http://127.0.0.1:5000 ...
start "RotaMais - API (porta 5000)" cmd /k python backend\app.py
echo.
echo [3/3] Iniciando o frontend em http://127.0.0.1:5500 ...
start "RotaMais - Frontend (porta 5500)" cmd /k python -m http.server 5500 --bind 127.0.0.1 --directory frontend
echo.
echo Abrindo o site no navegador. Para encerrar, feche as duas janelas abertas.
timeout /t 3 /nobreak >nul
start http://127.0.0.1:5500
