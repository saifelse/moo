import subprocess
from flask.ext.script import Manager
from moo import app

manager = Manager(app)

@manager.command
def compile(watch=True):
  flags = '-wco' if watch else '-co'
  coffee = subprocess.Popen('coffee %s moo/static/js moo/coffee' % flags, shell=True)

@manager.command
def scss():
  scss = subprocess.Popen('scss -w moo/scss:moo/static/css', shell=True)

if __name__ == "__main__":
    manager.run()
