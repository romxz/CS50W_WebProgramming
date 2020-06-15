import os

from flask import Flask, session, render_template, redirect, url_for
from flask_session import Session
from database import dbConnect

import requests

app = Flask(__name__)


# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = dbConnect.getDatabase()

# Goodreads
gk = ''


# Routes
@app.route("/")
def main():
    return render_template("public/index.html")

@app.route("/index.html", methods=["GET"])
def index():
    return render_template("public/index.html")

@app.route("/log_in.html", methods=["GET"])
def log_in():
    return render_template("public/log_in.html")#


#@app.route("/img/<string:loc>.png", methods=["GET"])
#def image(loc):
#    return redirect(url_for('static', filename=f'img/{loc}.png'))

@app.route("/js/<string:loc>.js", methods=["GET"])
def js(loc):
    if loc in ['scrolling', 'sliding']:
        return redirect(url_for('static', filename=f'js/{loc}.js'))
    else: return ''

@app.route("/css/<string:loc>.css", methods=["GET"])
def css(loc):
    return redirect(url_for('static', filename=f'css/{loc}.css'))

#@app.route("/img/<string:loc>.png", methods=["GET"])
#def img(loc):
#    return redirect(url_for('static', filename=f'img/{loc}.png'))#

# Other
def grapi():
    session['GRkey'] = session.get('GRkey', getGRkey())
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": session['GRkey'], "isbns": "9781632168146"})
    return f"Project 1: TODO\n{res.json()}"


def getGRkey():
    with open('.goodreads') as f:
        gk = f.readline().strip()
    return gk

#if __name__ == "__main__":
#    main()