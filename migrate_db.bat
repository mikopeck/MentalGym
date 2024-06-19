echo Activating virtual environment...
call venv\scripts\activate
echo Starting Flask...
call set FLASK_APP=backend\app.py
echo Starting migrate...
call flask db migrate
echo Starting upgrade...
call flask db upgrade
echo Done
pause