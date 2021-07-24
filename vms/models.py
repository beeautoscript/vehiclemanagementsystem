from datetime import datetime
from enum import unique
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from sqlalchemy.orm import backref
from vms import app,db,login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
	try:
		return Users.query.get(int(user_id))
	except:
		return None

# User Data Model
class Users(db.Model,UserMixin):
    __bind_key__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(5))
    password = db.Column(db.String(10),nullable=False)
    image_file = db.Column(db.String(20),nullable=False,default='default_user.png')
    registeredvehicle = db.relationship('RegisteredVehicle',backref='uservehicleregistered',cascade='all,delete-orphan')
    def __repr__(self):
        return f"Users('{self.username}')"

# Registered Vehicle
class RegisteredVehicle(db.Model):
    __bind_key__ = 'registeredvehicles'
    id = db.Column(db.Integer,primary_key=True)
    vehiclenum = db.Column(db.String(10),unique=True)
    tagid = db.Column(db.String(20),unique=True)
    ownername = db.Column(db.String(20),nullable=False)
    routeno = db.Column(db.Integer,nullable=False)
    makemodel = db.Column(db.Integer,nullable=False)
    registered_on = db.Column(db.DateTime(),nullable=False,default=datetime.now)
    entryexitimes = db.relationship('Entryexitime',backref="vechentryexitime")
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    
    def __repr__(self):
        return f"{self.vehiclenum}"

# Vehicle Entry Exit
class Entryexitime(db.Model):
    __bind_key__ = 'entryexitime'
    id = db.Column(db.Integer,primary_key=True)
    entrytime = db.Column(db.String(20))
    exitime = db.Column(db.String(20))
    registeredvehicle_id = db.Column(db.Integer,db.ForeignKey('registered_vehicle.id'))

# Vehicle On Premises
class VehicleOnPremises(db.Model):
    __bind_key__ = 'vehicleonpremises'
    id = db.Column(db.Integer,primary_key=True)
    tagid = db.Column(db.String(20),unique=True)
    status = db.Column(db.Boolean())
    entrytime = db.Column(db.String(20))
    exitime = db.Column(db.String(20))

    def __repr__(self):
        return f"{self.tagid,self.entrytime,self.exitime}"
