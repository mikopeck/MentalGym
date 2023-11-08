#!/bin/bash
# Activate the virtual environment
source backend/venv/bin/activate

# Start Gunicorn with the specified number of workers
gunicorn --workers=3 --bind=0.0.0.0:8000 --chdir backend app:app
