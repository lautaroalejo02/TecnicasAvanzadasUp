from flask import Flask, request, jsonify, Blueprint, session, current_app,render_template
import json
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mongoengine import MongoEngine
from apps.users.users import usersApp ,User #register_user
from apps.chats.chats import chatsApp
from flask_jwt_extended import JWTManager, create_access_token
from flask_socketio import SocketIO, send, emit
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'ChatAppTecnicasAvanzadas',
    'host': 'localhost',
    'port': 27017
}
app.config['allow_inheritance'] = True
db = MongoEngine()
db.init_app(app)
app.register_blueprint(usersApp, url_prefix='/api/users')
app.register_blueprint(chatsApp, url_prefix='/api/chats')
app.config["JWT_SECRET_KEY"] = "secret"  # Change this "super secret" with something else!
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)
userss = []
@app.route('/s')
def index():
    return render_template("index.html")



@socketio.on('message')
def handleMessage(msg, methods=['GET', 'POST']):
    print('Message: ' + msg)
    socketio.emit('message', msg)

@socketio.on('connect2')
def on_connect():
    msg="asdasd"
    print('Client connected')
    send(msg)


@socketio.on('sendMessage')
def handleMessage2(messageInfo):
    print(messageInfo)
    user = User.objects(userId=messageInfo['uID']).first()
    kala = {
        "_id": messageInfo['uID'], "chatRoom": messageInfo['crID'], "messageText": messageInfo['txtMsg'],
        "userName": user.name}
    userss.append(kala)
    print(userss)
    socketio.emit((userss))

if __name__ == '__main__':
    socketio.run(app, debug=True)
