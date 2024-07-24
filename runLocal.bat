cd frontend
echo Running npm build...
call npm run build
echo Build complete.
cd ..
echo Activating virtual environment...
call venv\scripts\activate
echo Starting Flask...
call set FLASK_APP=backend\app.py
call set RUN_SEEDING=False
call flask db upgrade
call set RUN_SEEDING=True
python backend\app.py
pause