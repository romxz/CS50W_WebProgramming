from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route("/")
def main():
    return render_template("public/index.html")

@app.route("/index.html")
def index():
    return render_template("public/index.html")

@app.route("/p<int:loc>.html")
def page(loc):
    return render_template(f"public/p{str(loc)}.html")

@app.route("/img/<string:loc>.png")
def image(loc):
    return redirect(url_for('static', filename=f'img/{loc}.png'))

@app.route("/js/<string:loc>.js")
def js(loc):
    if loc in ['scrolling', 'sliding']:
        return redirect(url_for('static', filename=f'js/{loc}.js'))
    else: return ''

@app.route("/css/<string:loc>.css")
def css(loc):
    return redirect(url_for('static', filename=f'css/{loc}.css'))