# import database instance
from ws import db
# db.init_app

# flask\Scripts\flask db init
# flask\Scripts\flask db migrate

# create database
# db.create_all()

# import classes
from ws.models import Tasks

# adding records
# tasks_1 = Tasks(title='What I like', description='Tesla, Colt, Boeing, Lockheed-Martin, SpaceX, DarkChild', done=0)
tasks_1 = Tasks(title='Shopping', description='Watch, shoes, clothing', done=0)
tasks_2 = Tasks(title='Travel', description='Anchorage, Appalachian Trail, Panama Canal', done=0)
tasks_3 = Tasks(title='Movies', description='6 Underground, Venom, Infinity War', done=1)
db.session.add(tasks_1)
db.session.add(tasks_2)
db.session.add(tasks_3)
db.session.commit()