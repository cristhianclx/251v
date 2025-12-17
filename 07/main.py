from flask import Flask
from flask import jsonify
from flask import request

from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["JWT_SECRET_KEY"] = "cibertec"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

jwt = JWTManager(app)


class User(db.Model):
    
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200), nullable=False)
    last_name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    country = db.Column(db.String(10), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<User: {}>".format(self.id) # <User: 1>
    

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref="user")

    def __repr__(self):
        return "<Message: {}>".format(self.id)  # <Message: 1>


class MessageBasicSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Message
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


message_basic_schema = MessageBasicSchema()
messages_basic_schema = MessageBasicSchema(many=True)


@app.route("/public")
def public():
    return {
        "public": True,
    }


@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "cristhian" or password != "password":
        return jsonify({"msg": "Bad username or password"}), 401
    access_token = create_access_token(identity="superuser")
    return jsonify(access_token=access_token)


@app.route("/me")
@jwt_required()
def me():
    return {
        "logged": get_jwt_identity(),
    }


@app.route("/messages")
@jwt_required()
def messages():
    username = get_jwt_identity()
    # LABORARIO
    # completar este EP, y si el usuario es superuser devolver todos los mensajes
    # si el usuario es otro, devolver los mensajes de ese usuario
    return {}