from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("public/index.html")

@app.route("/<string:loc>")
def page(loc):
    return render_template(f"public/{loc}")
