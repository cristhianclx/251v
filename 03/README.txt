# virtualenv

python -m venv .venv
.venv\Scripts\activate.bat # activate.ps

# install

pip install -r requirements.txt --upgrade

# utils

pip freeze
pip install flask

# run

flask --app main run --reload

# database

flask --app main db init # init
flask --app main db migrate # create migration (change in models)
flask --app main db upgrade # apply
flask --app main db downgrade # revert apply

# shell

flask --app main shell

>>> from main import db, Student
>>> item = Student(first_name="Alan", last_name="Garcia", age=50, country="PE", city="Lima")
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, Student
>>> Student.query.all()

>>> from main import db, Student
>>> Student.query.get_or_404(1)
>>> Student.query.filter_by(id=1).first()
>>> Student.query.filter_by(first_name="Alan").first()

>>> from main import db, Student
>>> item = Student.query.get_or_404(1)
>>> item.city = "Trujillo"
>>> db.session.add(item)
>>> db.session.commit()

>>> from main import db, Student
>>> item = Student.query.get_or_404(1)
>>> db.session.delete(item)
>>> db.session.commit()