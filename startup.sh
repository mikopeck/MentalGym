#!/bin/bash

pip install -r requirements.txt
flask db migrate
flask db upgrade

# Start Gunicorn with the specified number of workers
gunicorn --timeout 300 --workers=4 --bind=0.0.0.0:8000 --chdir backend app:app --log-level=info