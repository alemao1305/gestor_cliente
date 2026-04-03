from app import db

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.cpf'))
    date = db.Column(db.String(20))
    time = db.Column(db.Time)
    service = db.Column(db.String(100))

    client = db.relationship('Client', backref='appointments')