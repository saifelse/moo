from flask import Flask, render_template
app = Flask(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

@app.route("/")
def hello():
  return render_template('moo.jade')

if __name__ == "__main__":
  app.run()