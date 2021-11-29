from flask import Flask, request, jsonify, Blueprint, session
from werkzeug.security import check_password_hash, generate_password_hash
from apps.users.models import User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import secrets

app = Flask(__name__)
usersApp = Blueprint('usersApp', __name__)
jwt = JWTManager(app)

@usersApp.route('/register', methods = ["GET", "POST"])
def register_user():
    data = request.get_json(force=True)
    name = data["name"]
    email = data["email"]
    password = generate_password_hash(data["password"])
    user_to_register = User(name=name,
                email = email,
                password = password,
                )
    user_to_register.save()
    return "Exito!"

@usersApp.route('/login', methods = ["GET", "POST"])
def login_user():
    data = request.get_json(force = True)
    email = data['email']
    password = data['password']
    userToLogin = User.objects(email = email).first()
    if(check_password_hash(userToLogin.password, password )== True):
        access_token = create_access_token(identity=userToLogin.userId)
        updateUser = User.objects(email=email)
        updateUser.update(isConnected = True, chatRoomId = 0)
        return jsonify({"token": access_token, "user_id": userToLogin.userId})
    else:
        return "Invalid credentials", 401

@usersApp.route('/logout', methods = ["GET", "POST"])
@jwt_required()
def logout_user():
    current_user_id = get_jwt_identity()
    user = User.objects(userId = current_user_id).first()
    user.update(chatRoomId = 0)
    return jsonify({"id": user.id, "email": user.email}), 200

@usersApp.route('/enterChatroom', methods = ["POST"])
@jwt_required()
def enterChatroom():
    data = request.get_json(force = True)
    userId = data['userId']
    chatRoomId = data['chatRoomId']
    chatRoomEntered = User.objects(userId = userId)
    chatRoomEntered.update(chatRoomId = chatRoomId)
    connected_users = []
    for user in User.objects(chatRoomId = chatRoomId):
        connected_users.append(user)
    return jsonify(connected_users)

@usersApp.route('/connectedUsersList', methods = ["GET"])
def list_connected_users():
    chatRoomId = request.args.get("chatRoomId")
    connected_users = []
    for user in User.objects(chatRoomId = chatRoomId):
        connected_users.append(user)
    return jsonify(connected_users)