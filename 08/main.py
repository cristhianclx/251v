from flask import Flask, render_template, request, redirect, url_for
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

ma = Marshmallow(app)

socketio = SocketIO(app)


class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(220), nullable=False)
    status = db.Column(db.String(40), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return "<Project: {}>".format(self.id)


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Project
        load_instance = True
        datetimeformat = "%Y-%m-%d %H:%M:%S"


project_schema = ProjectSchema()
projects_schema = ProjectSchema(many=True)


@app.route("/status/")
def status():
    return {
        "status": "live"
    }


@app.route("/")
def index():
    items = Project.query.all()
    return render_template("index.html", items=items)


@socketio.on("ws-welcome")
def handle_ws_welcome(data):
    print("ws-welcome: " + str(data))


@app.route("/projects/add/", methods=["GET", "POST"])
def projects_add():
    if request.method == "GET":
        return render_template("projects-add.html")
    if request.method == "POST":
        item = Project(
            title = request.form["title"],
            description = request.form["description"],
            status = request.form["status"],
        )
        db.session.add(item)
        db.session.commit()
        socketio.emit("ws-projects-add", project_schema.dump(item))
        return render_template("projects-add.html", information="A new project has been added")
    

@app.route("/projects/<id>/edit/", methods=["GET", "POST"])
def projects_edit_by_id(id):
    data = Project.query.get_or_404(id)
    if request.method == "GET":
        return render_template("projects-edit.html", item=data)
    if request.method == "POST":
        data.title = request.form["title"]
        data.description = request.form["description"]
        data.status = request.form["status"]
        db.session.add(data)
        db.session.commit()
        socketio.emit("ws-projects-edit", project_schema.dump(data))
        return render_template("projects-edit.html", item=data, information="Your changes were saved")


@app.route("/projects/<id>/delete/", methods=["GET", "POST"])    
def projects_delete_by_id(id):
    data = Project.query.get_or_404(id)
    if request.method == "GET":
        return render_template("projects-delete.html", item=data)
    if request.method == "POST":
        db.session.delete(data)
        db.session.commit()
        socketio.emit("ws-projects-delete", {"id": id})
        return redirect(url_for('index'))
    

# LABORATORIO:
# Implementar websockets para los ejemplos que ya vimos de Students/Messages
# de modo que luego de agregar, editar o borrar se pueda ver lo mismo en el listado