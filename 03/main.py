from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)


class Student(db.Model):
    
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    country = db.Column(db.String(10))
    city = db.Column(db.String(50))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Student: {}>".format(self.id) # <Student: 1>


class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    student_id = db.Column(db.Integer, db.ForeignKey("students.id"))
    student = db.relationship("Student", backref="student")

    def __repr__(self):
        return "<Message: {}>".format(self.id) # <Message: 1>



@app.route("/status/")
def status():
    return {
        "status": "live"
    }