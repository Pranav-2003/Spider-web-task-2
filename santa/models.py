from datetime import datetime
from email.policy import default
from enum import unique
from santa import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    city = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(3), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    group = db.relationship('Group', backref='owner', lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class Group(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    code = db.Column(db.String(5), nullable=False, unique=True)
    date = db.Column(db.DateTime, nullable=False)
    cdate = db.Column(db.DateTime, nullable=False, default=datetime.now())
    budget = db.Column(db.String(6), nullable=False)
    location = db.Column(db.String(15), nullable=False)
    members = db.relationship('Members',backref='group', lazy=True)
    
    def __repr__(self):
        return f"Group('{self.name}')"
    
class Members(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    gno = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=False)
    gname = db.Column(db.String(30), nullable=False)
    uid = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f"Group('{self.gno}','{self.name}')"