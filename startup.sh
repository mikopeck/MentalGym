#!/bin/bash

pip install -r requirements.txt
flask db upgrade

flask shell <<EOF
from sqlalchemy import MetaData
meta = MetaData(bind=db.engine)
meta.reflect()
for table in meta.tables.values():
    print(table)
EOF

# Start Gunicorn with the specified number of workers
gunicorn --workers=3 --bind=0.0.0.0:8000 --chdir backend app:app