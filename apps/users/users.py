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
    name = request.args.get("name")
    email = request.args.get("email")
    password = generate_password_hash(request.args.get("password"))
    profilePic = request.args.get("profilePicture")
    user_to_register = User(name=name,
                email = email,
                password = password,
                profilePicture = profilePic,
                )
    user_to_register.save()
    return "Exito!"

@usersApp.route('/login', methods = ["GET", "POST"])
def login_user():
    userToLogin = User.objects(email = request.args.get("email")).first()
    if(check_password_hash(userToLogin.password, request.args.get("password")) == True):
        access_token = create_access_token(identity=userToLogin.userId)
        return jsonify({"token": access_token, "user_id": userToLogin.userId})
    else:
        return "Invalid credentials", 401

@usersApp.route('/logout', methods = ["GET", "POST"])
@jwt_required()
def logout_user():
    current_user_id = get_jwt_identity()
    user = User.objects(userId = current_user_id).first()

    return jsonify({"id": user.id, "email": user.email}), 200

@usersApp.route('/enterChatroom', methods = ["POST"])
@jwt_required()
def enterChatroom():
    userId = request.args.get("userId")
    chatRoomId = request.args.get("chatRoomId")
    chatRoomEntered = User.objects(userId = userId)
    User.update(chatRoomId = chatRoomId)
    return "User entered the chatRoom"

@usersApp.route('/connectedUsersList', methods = ["POST"])
@jwt_required()
def list_connected_users():
    userId = request.args.get("userId")
    chatRoomId = request.args.get("chatRoomId")
    user_to_connect = User.objects(userId = userId)
    user_to_connect.update(chatRoomId = chatRoomId)
    return "User entered the chatRoom"