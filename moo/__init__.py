import json
import sqlite3
from flask import Flask, g, render_template, Response, request, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moo.db'


# Configure database
db = SQLAlchemy(app)

class Puzzle(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  level = db.Column(db.Integer, unique=True)
  name = db.Column(db.String(255))
  password = db.Column(db.String(255))
  metakey = db.Column(db.Integer, nullable=True)
  solved = db.Column(db.Boolean, default=False)
  unlocked = db.Column(db.Boolean, default=False)
  template = db.Column(db.String(255))

  def to_dict(self):
    d = {
      'id': self.id,
      'level': self.level,
      'name': self.name,
      'metakey': self.metakey,
      'length': len(self.password),
      'solved': self.solved,
      'solve_url': url_for('solve_puzzle', puzzle_id=self.id)
    }
    if self.unlocked:
      d['html'] = render_template(self.template)
    if self.solved:
      d['password'] = self.password
    return d

def reset_db():
  db.create_all()
  puzzles = [
    Puzzle(level=1, name='Hey diddle diddle,', password='HI', metakey=0, unlocked=True, template='level1.jade'),
    Puzzle(level=2, name='The Cat and the Fiddle,', password='BAA', metakey=1, template='level2.jade'),
    Puzzle(level=3, name='The Cow jumped over the Moon.', password='BARK', metakey=2, template='level3.jade'),
    Puzzle(level=4, name='The Little Dog laughed to see such sport,', password='SPOON', metakey=1, template='level4.jade'),
    Puzzle(level=5, name='And the Dish ran away with the Spoon', password='GITHUB', metakey=-1, template='level5.jade')
  ]
  for puzzle in puzzles:
    db.session.add(puzzle)
  db.session.commit()


@app.route('/')
def hello():
  return render_template('moo.jade')

# AJAX endpoints
@app.route('/api/puzzles', methods=['GET'])
def unlocked_puzzles():
  puzzles = Puzzle.query.filter_by(unlocked=True).order_by(Puzzle.level)
  info = [puzzle.to_dict() for puzzle in puzzles]
  return Response(json.dumps(info), content_type='application/json'), 200

@app.route('/api/puzzles/<puzzle_id>', methods=['GET'])
def puzzle(puzzle_id):
  puzzle = Puzzle.query.filter_by(id=puzzle_id, unlocked=True).first()
  if puzzle is None:
    error = {'message': 'Unable to locate the requested puzzle.'}
    return Response(json.dumps(error), content_type='application/json'), 404
  else:
    return Response(json.dumps(puzzle.to_dict()), content_type='application/json'), 200

@app.route('/api/puzzles/<puzzle_id>/solve', methods=['POST'])
def solve_puzzle(puzzle_id):
  status_code = 200
  message = ''

  print request.form
  if request.form is None:
    password = None
  else:
    password = request.form.get('password', None)

  puzzle = Puzzle.query.filter_by(id=puzzle_id, unlocked=True).first()

  if password is None:
    status_code = 400
    message = 'You didn\'t submit a password!'
  elif puzzle is None:
    status_code = 400
    message = 'The specified puzzle doesn\'t exist!'
  elif not (password == puzzle.password):
    print `password`, `puzzle.password`
    status_code = 403
    message = 'Oops. Wrong password!'

  if status_code is not 200:
    error = {'message': message}
    return Response(json.dumps(error), content_type='application/json'), status_code

  # Otherwise, we are in the clear! Unlock the next level and return it.
  puzzle.solved = True
  db.session.add(puzzle)

  next_puzzle = Puzzle.query.filter_by(level=(puzzle.level + 1)).first()

  info = {'puzzle': puzzle.to_dict()}
  if next_puzzle is not None:
    next_puzzle.unlocked = True
    db.session.add(next_puzzle)
    info['next_puzzle'] = next_puzzle.to_dict()
    info['message'] = 'You\'ve unlocked the next puzzle!'
  else:
    info['message'] = 'Welp, you\'ve finished all the puzzles. Hope you had fun :)'
  db.session.commit()
  return Response(json.dumps(info), content_type='application/json'), status_code


if __name__ == "__main__":
  app.run()
