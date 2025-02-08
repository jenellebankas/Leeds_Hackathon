from app import db

class Assessment(db.Model):
    id  =  db.Column(db.Integer, primary_key = True)
    assessment_title = db.Column(db.String(50), nullable = False)
    module_code = db.Column(db.String(10), nullable = False)
    deadline_date = db.Column(db.DateTime, nullable = False)
    description = db.Column(db.String(200))
    status = db.Column(db.Boolean, default = False)