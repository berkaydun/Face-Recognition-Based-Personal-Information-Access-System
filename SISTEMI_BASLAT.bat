@echo off
echo RUNNING... PLEASE WAIT...
echo BROWSER WILL OPEN AND SYSTEM WILL BE READY.
echo DO NOT CLOSE THIS WINDOW. TO STOP THE SYSTEM, YOU CAN CLOSE THIS WINDOW.

cd /d "%~dp0"
call .venv\Scripts\activate

start "" "http://127.0.0.1:5000"

python app.py
pause
