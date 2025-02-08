@echo off
REM Activate the Anaconda Flask environment
conda activate flask

REM Set Flask environment variables
set FLASK_APP=run.py
set FLASK_DEBUG=1

REM Run Flask development server
flask run
