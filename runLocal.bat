cd frontend
echo Running npm build...
call npm run build
echo Build complete.
cd ..
echo Activating virtual environment...
call venv\scripts\activate
echo Starting Flask...
set PYTHON_APP=backend\app.py
flask db upgrade
python backend\app.py