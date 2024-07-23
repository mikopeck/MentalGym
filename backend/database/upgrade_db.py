from database.models import db, User, Library
import os

def run_upgrades():
    if os.getenv('RUN_SEEDING', 'False') == 'True':
        upgrade_user_exp()
        upgrade_library_socials()



# upgradess

def upgrade_user_exp():
    users = User.query.filter(User.experience_points == None).all()
    for user in users:
        user.experience_points = 0

    db.session.commit()

def upgrade_library_socials():
    libraries = Library.query.filter(Library.clicks == None).all()
    for library in libraries:
        library.clicks = 0

    libraries = Library.query.filter(Library.likes == None).all()
    for library in libraries:
        library.likes = 0