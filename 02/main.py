from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://user:password@localhost/database"

db.init_app(app)


class Student(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    age: Mapped[int]


with app.app_context():
    db.create_all()