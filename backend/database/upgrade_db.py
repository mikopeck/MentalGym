from database.models import db, User
import os

def run_upgrades():
    if os.getenv('RUN_SEEDING', 'False') == 'True':
        upgrade_user_exp()



# upgradess

def upgrade_user_exp():
    users = User.query.filter(User.experience_points == None).all()
    for user in users:
        user.experience_points = 0

    db.session.commit()