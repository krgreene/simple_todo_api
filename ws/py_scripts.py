# import database instance
from ws import db

# create database
db.create_all()

# import classes
from models import Tasks

# adding records
tasks_1 = Tasks(title='What I like', description='Tesla, Colt, Boeing, Lockheed-Martin, SpaceX, DarkChild', done=0)

db.session.add(tasks_1)
db.session.commit()