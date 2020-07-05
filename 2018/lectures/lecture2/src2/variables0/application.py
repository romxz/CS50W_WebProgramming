from flask import Flask, render_template

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
    headline = "Hello, world!"
    return render_template("index.html", headline=headline)

@app.route("/bye")
def bye():
    headline = "Goodbye!"
    return render_template("index.html", headline=headline)