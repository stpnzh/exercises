from flask import render_template, url_for, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_marshmallow import Marshmallow

from app import app
from app import db
from app.models import Exercise
from app.forms import LoginForm


@app.route('/', methods=['GET', 'POST'])
def index():
  if request.method == 'POST':
    target_body = request.form['choose']
  else:
    target_body = 'upper'
 
  exercises = Exercise.query.order_by(func.lower(Exercise.name)).all()

  # exercises = db.engine.execute('SELECT * FROM Exercise ORDER BY name COLLATE NOCASE ASC')

  def get_exercise(type):
    if type=='pull' or type=='push':
      return Exercise.query.filter_by(body_area=type).order_by(func.random()).first()
    else:
      return Exercise.query.filter_by(body_area=type).order_by(func.random()).first()

  def get_other_exercise():
    return Exercise.query.filter((Exercise.body_area == 'full') | (Exercise.body_area == 'distance')).order_by(func.random()).first()

  d1 = get_exercise('push')
  d2 = get_exercise('push')
  d3 = get_exercise('pull')
  d4 = get_exercise('pull')
  d5 = get_exercise('core')
  d6 = get_exercise('legs')
  d7 = get_other_exercise()
  d8 = get_other_exercise()

  while d1 == d2:
    d1 = get_exercise('push')

  while d3 == d4:
    d3 = get_exercise('pull')

  while d7 == d8:
    d7 = get_other_exercise()


  return render_template('index.html', 
  exercises=exercises, 
   d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, d6=d6, d7=d7, d8=d8, 
   target_body=target_body)


@app.route('/exercises', methods=['POST', 'GET'])
def exercises():
  if request.method == 'POST':
    exercise_name = request.form['name']
    exercise_body_area = request.form['body_area']
    new_exercise = Exercise(name=exercise_name, body_area=exercise_body_area)

    try:
      db.session.add(new_exercise)
      db.session.commit()
      return redirect('/exercises')
    except:
      return 'Error!'

  else:
    exercises = Exercise.query.order_by(Exercise.name).all()

    def count_exercises(type):
      return Exercise.query.filter(Exercise.body_area==type).count()

    return render_template('exercises.html', 
    exercises=exercises, 
    push_count=count_exercises('push'),
    pull_count=count_exercises('pull'),
    legs_count=count_exercises('legs'),
    core_count=count_exercises('core'),
    full_count=count_exercises('full'),
    distance_count=count_exercises('distance')
    )


@app.route('/delete/<int:id>')
def delete(id):
  exercise_to_delete = Exercise.query.get_or_404(id)
  
  try:
    print(exercise_to_delete.name)
    db.session.delete(exercise_to_delete)
    print(exercise_to_delete.name)
    db.session.commit()
    return redirect('/exercises')
  except:
    return 'Error in deletion!'


# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#   exercise = Exercise.query.get_or_404(id)

#   if request.method == 'POST':
#     exercise.name = request.form['name']
#     exercise.body_area = request.form['body_area']

#     try:
#       db.session.commit()
#       return redirect('/exercises')
#     except:
#       return 'Error in updating!'

#   else:
#     return render_template('update.html', exercise=exercise)
    

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    flash('Login requested for user {}, remember_me={}'.format(
      form.username.data, form.remember_me.data))
    return redirect('/')
  return render_template('login.html', form=form)