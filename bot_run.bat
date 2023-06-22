@echo off

call %~dp0telegram_bot\venv\Scripts\activate

cd %~dp0telegram_bot

set TOKEN=6145976588:AAFh4LEA1iikYr_nvzHseul9JdYoWp0rLGI

python bot_telegram.py

pause