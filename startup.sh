#!/bin/bash

echo "Installing requirements..."
pip install -r requirements.txt

export FLASK_ENV=production

echo "Starting database upgrade..."
flask db upgrade
if [ $? -ne 0 ]; then
    echo "Database upgrade failed"
    exit 1
else
    echo "Database upgrade successful"
fi

# Start Gunicorn with the specified number of workers
echo "Starting Gunicorn server..."
gunicorn --timeout 300 --workers=4 --bind=0.0.0.0:8000 --chdir backend app:app --log-level=info