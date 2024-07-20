from database.models import db, User

def run_upgrades():
    upgrade_user_exp()



# upgradess

def upgrade_user_exp():
    users = User.query.filter(User.experience_points == None).all()
    for user in users:
        user.experience_points = 0

    db.session.commit()