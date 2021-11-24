from db_init import db
from datetime import date

class User(db.Document):
    userId = db.SequenceField(primary_key=True)
    name = db.StringField(required = True)
    email = db.EmailField(required = True)
    password = db.StringField(required = True)
    profilePicture = db.ImageField(default = "noPic", required = False)
    registerDate = db.DateTimeField(required = True, default = date.today())
    chatRoomId = db.IntField(required = True, default = 0)
    isConnected = db.BooleanField(default = False)