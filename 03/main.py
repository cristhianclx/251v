from flask import Flask, render_template, request, redirect, url_for
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


@app.route("/students/")
def students():
    data = Student.query.all()
    return render_template("students.html", items=data)


@app.route("/students/add/", methods=["GET", "POST"])
def students_add():
    if request.method == "GET":
        return render_template("students_add.html")
    if request.method == "POST":
        item = Student(
            first_name=request.form["first_name"],
            last_name=request.form["last_name"],
            age=request.form["age"],
            country=request.form["country"],
            city=request.form["city"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("students_add.html", information="Your changes were saved")


@app.route("/students/<id>")
def students_by_id(id):
    data = Student.query.get_or_404(id)
    return render_template("students_details.html", item=data)


@app.route("/students/<id>/edit/", methods=["GET", "POST"])
def students_edit_by_id(id):
    data = Student.query.get_or_404(id)
    if request.method == "GET":
        return render_template("students_edit.html", item=data)
    if request.method == "POST":
        data.first_name = request.form["first_name"]
        data.last_name = request.form["last_name"]
        data.age = request.form["age"]
        data.country = request.form["country"]
        data.city = request.form["city"]
        db.session.add(data)
        db.session.commit()
        return render_template("students_edit.html", item=data, information="Your changes were saved")


@app.route("/students/<id>/delete/", methods=["GET", "POST"])
def students_delete_by_id(id):
    data = Student.query.get_or_404(id)
    if request.method == "GET":
        return render_template("students_delete.html", item=data)
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('students'))


@app.route("/messages/")
def messages():
    data = Message.query.all()
    return render_template("messages.html", items=data)


@app.route("/messages/add/", methods=["GET", "POST"])
def messages_add():
    students = Student.query.all()
    if request.method == "GET":
        return render_template("messages_add.html", students=students)
    if request.method == "POST":
        item = Message(
            title=request.form["title"],
            content=request.form["content"],
            student_id=request.form["student_id"],
        )
        db.session.add(item)
        db.session.commit()
        return render_template("messages_add.html", students=students, information="Your changes were saved")


@app.route("/messages/<id>")
def messages_by_id(id):
    data = Message.query.get_or_404(id)
    return render_template("messages_details.html", item=data)


@app.route("/messages/<id>/edit/", methods=["GET", "POST"])
def messages_edit_by_id(id):
    students = Student.query.all()
    data = Message.query.get_or_404(id)
    if request.method == "GET":
        return render_template("messages_edit.html", students=students, item=data)
    if request.method == "POST":
        data.title = request.form["title"]
        data.content = request.form["content"]
        data.student_id = request.form["student_id"]
        db.session.add(data)
        db.session.commit()
        return render_template("messages_edit.html", students=students, item=data, information="Your changes were saved")


@app.route("/messages/<id>/delete/", methods=["GET", "POST"])
def messages_delete_by_id(id):
    data = Message.query.get_or_404(id)
    if request.method == "GET":
        return render_template("messages_delete.html", item=data)
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('messages'))