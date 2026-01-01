from flask import Flask, session, render_template, redirect, url_for
from flask_session import Session 
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/")
def index():
    if "board" and "turn" not in session:
        session["board"] = [[None, None, None], 
                            [None, None, None], 
                            [None, None, None]]
        session["turn"] = "X"
        session['started'] = True
    return render_template("game.html", game=session["board"], turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row, col):
    if session.get('started'):
        session["board"][row][col] = session["turn"]
        if session["turn"] == 'X':
            session["turn"] = 'O'
        else: 
            session["turn"] = 'X';    
    return redirect(url_for("index"))

@app.route("/reset")
def reset():
     session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
     session.pop('turn', None)
     session.pop('started', None)
     return redirect(url_for("index"))