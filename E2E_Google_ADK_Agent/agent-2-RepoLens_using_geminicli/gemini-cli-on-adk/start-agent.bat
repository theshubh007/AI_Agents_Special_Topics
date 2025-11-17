@echo off
echo Starting Gemini CLI ADK Agent...
echo.
echo Once started, open your browser to: http://localhost:8080
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
adk web --host 127.0.0.1 --port 8080 .
