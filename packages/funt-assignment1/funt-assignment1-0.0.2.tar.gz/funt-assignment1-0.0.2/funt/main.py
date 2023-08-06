from datetime import datetime
from pathlib import Path

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import numpy as np
import sqlalchemy


db_dir = Path(__file__).parent
db_file = db_dir / Path('funt.sqlite')
db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_file}"
db.init_app(app)


class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    grade = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Exam %r>' % self.id


with app.app_context():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        exam_name = request.form['courseName']
        exam_grade = request.form['examMark']
        new_exam = Exam(name=exam_name, grade=exam_grade)
        try:
            db.session.add(new_exam)
            db.session.commit()
            db.session.close()
            return redirect('/')
        except sqlalchemy.exc.SQLAlchemyError:
            return 'There was an issue adding your exam'
    else:
        exams = db.session.query(Exam).order_by(Exam.date_created).all()
        return render_template("index.html", exams=exams)


@app.route("/grades-mean", methods=['GET'])
def mean():
    exams = db.session.query(Exam).order_by(Exam.date_created).all()
    grades = []
    for e in exams:
        grades.append(int(e.grade))
    grades_mean = round(np.mean(grades), 2)
    return render_template("mean.html", mean=grades_mean)
