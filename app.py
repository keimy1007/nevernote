# An attempt to rewrite entire program with Flask
from flask import Flask, render_template


app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return "petrp"

    


    