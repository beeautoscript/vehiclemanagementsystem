from vms import db
from vms.models import Users
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

hashpass = bcrypt.generate_password_hash('user1234').decode('utf-8')

user = Users(username="user1",password=hashpass)

db.session.add(user)
db.session.commit()

