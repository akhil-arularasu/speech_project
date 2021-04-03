from flask import Flask, redirect, url_for, render_template, request, Response, session
from textblob import TextBlob
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io
import random
import numpy as np
import math
import pandas as pd

app = Flask(__name__)
app.secret_key = "hello"

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

@app.route('/plot.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    polarity_transcript = []
    if "polarity_transcript" in session:
        polarity_transcript = session["polarity_transcript"]
        print(polarity_transcript)
    axis = fig.add_subplot(1, 1, 1)
    xs = range(10)
    ys = [random.randint(1, 50) for x in xs]
    print(xs)
    print(ys)
    print(polarity_transcript)
    axis.plot(xs,polarity_transcript[0])
    return fig

def split_text(text, n=10):
    # Calculate length of text, the size of each chunk of text and the starting points of each chunk of text
    length = len(text)
    size = math.floor(length / n)
    start = np.arange(0, length, size)

    # Pull out equally sized pieces of text and put it into a list
    split_list = []
    for piece in range(n):
        split_list.append(text[start[piece]:start[piece]+size])
    return split_list

@app.route("/speech", methods=["POST", "GET"])
def speech():
    if request.method == "POST":
        speech_script = request.form["speech_script"]
        speech_data = {'transcript': [speech_script]}
        data = pd.DataFrame(speech_data, columns = ['transcript'])
        testimonial = TextBlob(speech_script)
# Let's create a list to hold all of the pieces of text
        list_pieces = []
        for t in data.transcript:
            split = split_text(t)
            list_pieces.append(split)
        polarity_transcript = []
        for lp in list_pieces:
            polarity_piece = []
            for p in lp:
                polarity_piece.append(TextBlob(p).sentiment.polarity)
            polarity_transcript.append(polarity_piece)

        print(polarity_transcript)
        session["polarity_transcript"] = polarity_transcript
        return render_template("speech_analysis.html", script=speech_script, sentiment=testimonial.sentiment)
    else:
        return render_template("speech.html")

@app.route("/<usr>")
def user(usr):
    return render_template("index.html", user=usr)



if __name__ == "__main__":
    app.run(debug=True)
