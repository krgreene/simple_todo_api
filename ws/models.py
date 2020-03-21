from ws import db

# database tables
        
class Tasks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(1000), nullable=True)
    done = db.Column(db.Integer, nullable=True)

    def to_json(self):
        return {'id':self.id, 'title':self.title, 'description':self.description, 'done':self.done}   

