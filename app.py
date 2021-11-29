from flask import Flask, request, jsonify, Blueprint, session, current_app, render_template
import json
import hashlib
from werkzeug.security import check_password_hash, generate_password_hash
from flask_mongoengine import MongoEngine
from apps.users.users import usersApp ,register_user
from apps.chats.chats import chatsApp
from flask_jwt_extended import JWTManager, create_access_token
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)
app.config['MONGODB_SETTINGS'] = {
    'db': 'ChatAppTecnicasAvanzadas',
    'host': 'localhost',
    'port': 27017
}
app.config['allow_inheritance'] = True
db = MongoEngine()
db.init_app(app)
app.register_blueprint(usersApp)
app.register_blueprint(chatsApp)
app.config["JWT_SECRET_KEY"] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg"  # Change this "super secret" with something else!
jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    send(msg, broadcast = True)

if __name__ == '__main__':
    app.run()
