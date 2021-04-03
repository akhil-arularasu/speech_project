from flask import Flask, redirect, url_for, render_template, request
from textblob import TextBlob

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["nm"]
        return render_template("welcome.html", user=user)
    else:
        return render_template("login.html")

@app.route("/speech", methods=["POST", "GET"])
def speech():
    if request.method == "POST":
        speech_script = request.form["speech_script"]
        print(speech_script)
        testimonial = TextBlob(speech_script)
        print(testimonial.sentiment)
        return render_template("speech_analysis.html", script=speech_script, sentiment=testimonial.sentiment)
    else:
        return render_template("speech.html")

@app.route("/<usr>")
def user(usr):
    return render_template("index.html", user=usr)



if __name__ == "__main__":
    app.run(debug=True)
