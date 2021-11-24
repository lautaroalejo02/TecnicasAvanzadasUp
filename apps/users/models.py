from db_init import db
from datetime import date

class User(db.Document):
    userId = db.SequenceField(primary_key=True)
    name = db.StringField()
    email = db.EmailField()
    password = db.StringField()
    profilePicture = db.ImageField(default = "noPic", required = False)
    registerDate = db.DateTimeField(required = True, default = date.today())
    chatRoomId = db.IntField(required = True, default = 0)
    isConnected = db.BooleanField(default = False)