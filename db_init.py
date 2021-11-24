from flask_mongoengine import MongoEngine
db = MongoEngine()
meta = {'allow_inheritance': True}
def init_app(app):
    db.init_app(app)