from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    admin_name = db.Column(db.String(255))
    admin_phone = db.Column(db.String(20))
    members = db.relationship('Member', backref='group', lazy=True)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
