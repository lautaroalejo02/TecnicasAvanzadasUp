from flask import Flask, request, jsonify, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import secrets
from apps.chats.models import ChatRoom, Message

app = Flask(__name__)
chatsApp = Blueprint('chatsApp', __name__)

@chatsApp.route('/addChatRoom', methods = ["POST"])
@jwt_required()
def create_chatRoom():
    name = request.args.get("name")
    chatRoomToAdd = ChatRoom(chatRoomName=name)
    chatRoomToAdd.save()
    return "Exito!"

@chatsApp.route('/sendMessage', methods = ["POST"])
@jwt_required()
def send_message():
    messageText = request.args.get("messageText")
    userId = request.args.get("userId")
    chatRoomId = request.args.get("chatRoomId")
    messageToAdd = Message(messageText=messageText, userId = userId, chatRoomId = chatRoomId)
    messageToAdd.save()
    return "Message sent"

@chatsApp.route('/listMessages', methods = ["POST"])
@jwt_required()
def list_messages():
    Message.objects.all()
    return "Message sent"

@chatsApp.route('/listChatRoom', methods = ["GET"])
@jwt_required()
def list_chatRooms():
    chatRooms = []
    for chat in ChatRoom.objects.all():
        chatRooms.append(chat)
    return jsonify(chatRooms)