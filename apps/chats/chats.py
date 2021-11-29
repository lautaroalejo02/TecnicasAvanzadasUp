from flask import Flask, request, jsonify, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import secrets
from flask_socketio import SocketIO, send
from apps.chats.models import ChatRoom, Message
from mongoengine.queryset.visitor import Q

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
    data = request.get_json(force=True)
    messageText = data['messageText']
    userId = data['userId']
    chatRoomId = data['chatRoomId']
    messageToAdd = Message(messageText=messageText, userId = userId, chatRoomId = chatRoomId)
    messageToAdd.save()
    return "Message sent",200

@chatsApp.route('/listMessages', methods = ["GET"])
def list_messages():
    data = request.get_json(force = True)
    chatRoom = data['chatRoomId']
    messages = []
    for message in Message.objects(chatRoomId=chatRoom):
        messages.append(message)
    return jsonify(messages)

@chatsApp.route('/delete-messages', methods = ["DELETE"])
def delete_all_messages():
    data = request.get_json(force = True)
    userId = data['userId']
    chatRoomId = data['chatRoomId']
    Message.objects(Q(userId=userId) & Q(chatRoomId=chatRoomId)).delete()
    return "All messages deleted"

@chatsApp.route('/listChatRoom', methods = ["GET"])
def list_chatRooms():
    chatRooms = []
    for chat in ChatRoom.objects.all():
        chatRooms.append(chat)
    return jsonify(chatRooms)

