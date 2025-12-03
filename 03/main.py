from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Student(db.Model):
    
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    age = db.Column(db.Integer)
    country = db.Column(db.String(10))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Student: {}>".format(self.id) # <Student: 1>


@app.route("/status/")
def status():
    return {
        "status": "live"
    }


# en el modelo Student, agregar una columna city, String(50)