#!/bin/bash
# Activate the virtual environment
cd backend
source venv/bin/activate

# Start Gunicorn with the specified number of workers
gunicorn --workers=1 --bind=0.0.0.0:8000 app:app
