from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import AscendanceUser  # Import your User model

# Replace 'sqlite:///your_database.db' with your actual database URI
DATABASE_URI = 'mysql+pymysql://root:password@localhost/mind_forge_ai'

# Connect to the database using SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Query all users
users = session.query(AscendanceUser).all()

# Apply default values to users if they are None
for user in users:
    if user.confirmed is None:
        user.confirmed = True

# Commit the changes to the database
session.commit()

# Close the session
session.close()
