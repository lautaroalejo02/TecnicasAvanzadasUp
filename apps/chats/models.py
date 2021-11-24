from mongoengine import ReferenceField
from db_init import db
from datetime import date
from apps.users.models import User

class ChatRoom(db.Document):
    chatRoomId = db.SequenceField(primary_key=True)
    chatRoomName = db.StringField(required = True)

class Message(db.Document):
    messageId = db.SequenceField(primary_key=True)
    messageText = db.StringField(required = True)
    userId = ReferenceField(User)
    chatRoomId = ReferenceField(ChatRoom)
    sentDate = db.DateTimeField(required = True, default = date.today())