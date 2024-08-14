from database.models import db, User, Library
import os

def run_upgrades():
    if os.getenv('RUN_SEEDING', 'False') == 'True':
        upgrade_user_exp()
        upgrade_library_socials()
        upgrade_lib_imgs()
        upgrade_lib_guide()
        db.session.commit()



# upgradess

def upgrade_user_exp():
    users = User.query.filter(User.experience_points == None).all()
    for user in users:
        user.experience_points = 0

def upgrade_library_socials():
    libraries = Library.query.filter(Library.clicks == None).all()
    for library in libraries:
        library.clicks = 0

    libraries = Library.query.filter(Library.likes == None).all()
    for library in libraries:
        library.likes = 0

def upgrade_lib_imgs():
    libraries = Library.query.filter(Library.image_url == None).all()
    for library in libraries:
        library.image_url = "https://csb10032002fc59a9f5.blob.core.windows.net/library-images/background.png"

    libraries = Library.query.filter(Library.image_url == '').all()
    for library in libraries:
        library.image_url = "https://csb10032002fc59a9f5.blob.core.windows.net/library-images/background.png"

def upgrade_lib_guide():
    libraries = Library.query.filter(Library.guide == None).all()
    for library in libraries:
        library.guide = "Azalea"