from flask import Flask, render_template, request, session
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

notes = []  # Could use as global variable but not good
# Use session['notes'] instead

@app.route("/", methods=["GET", "POST"])
def index():
    #if session.get("notes") is None:
    #    session["notes"] = []
    session["notes"] = session.get("notes", [])
    if request.method == "POST":
        note = request.form.get("note")
        # notes.append(note)
        session["notes"].append(note)

    return render_template("index.html", notes=session['notes'])
    #return render_template("index.html", notes=notes)

@app.route("/clear", methods=["GET"])
def clear():
    # notes.clear()
    session['notes'] = session.get('notes', [])
    session['notes'].clear()
    return render_template("index.html", notes=session['notes'])
    #return render_template("index.html", notes=notes)
