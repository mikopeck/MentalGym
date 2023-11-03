from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import User  # Import your User model

# Replace 'sqlite:///your_database.db' with your actual database URI
DATABASE_URI = 'mysql+pymysql://root:password@localhost/mind_forge_ai'

# Connect to the database using SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Default values
DEFAULT_TIER = 'free'
DEFAULT_DAILY_REQUEST_COUNT = 0
DEFAULT_LAST_REQUEST_TIME = datetime.utcnow()
DEFAULT_VIOLATION_COUNT = 0

# Query all users
users = session.query(User).all()

# Apply default values to users if they are None
for user in users:
    if user.tier is None:
        user.tier = DEFAULT_TIER
    if user.daily_request_count is None:
        user.daily_request_count = DEFAULT_DAILY_REQUEST_COUNT
    if user.last_request_time is None:
        user.last_request_time = DEFAULT_LAST_REQUEST_TIME
    if user.violation_count is None:
        user.violation_count = DEFAULT_VIOLATION_COUNT

# Commit the changes to the database
session.commit()

# Close the session
session.close()
