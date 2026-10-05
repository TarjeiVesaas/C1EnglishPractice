from flask import Flask, request, session, redirect, url_for, render_template
import os

from gameLogic import (
    load_verbs,
    pick_random_phrasal_verb,
    check_particle,
    full_phrasal_verb,
    PhrasalVerb
)

app = Flask("C1EnglishPractice")
app.secret_key = os.environ.get("SECRET_KEY", "dev-key")

verbs = load_verbs("Phrasal Verbs")

current = pick_random_phrasal_verb(verbs)

@app.route("/set_name", methods=["GET", "POST"])
def set_name():

    feedback = ""

    if request.method == "POST":
        name = request.form.get("name", "").strip()

        if name:
            session["player_name"] = name

            if "points" not in session:
                session["points"] = 0
                session["guesses"] = 0

            return redirect(url_for("select_game"))

        feedback = "Please enter your name!"

    return render_template(
        "set_name.html",
        feedback=feedback
    )

@app.route("/select_game", methods=["GET", "POST"])
def select_game():

    if "player_name" not in session:
        return redirect(url_for("set_name"))

    if request.method == "POST":

        game_type = request.form.get("game_type")

        if game_type == "phrasal_verbs":
            session["game_type"] = game_type
            return redirect(url_for("play"))

        elif game_type == "phrasal_meanings":

            return """
            <html>
            <head>
                <title>Coming Soon</title>

                <style>

                    body{
                        background:#121212;
                        color:white;
                        font-family:Segoe UI;
                        text-align:center;
                        padding:80px;
                    }

                    a{
                        color:#3498db;
                        font-size:1.3em;
                        text-decoration:none;
                    }

                </style>

            </head>

            <body>

                <h1>🚧 Coming Soon!</h1>

                <h2>Phrasal Verb Meanings is still under development.</h2>

                <br>

                <a href="/select_game">← Back</a>

            </body>

            </html>
            """

    return render_template(
        "select_game.html",
        player_name=session["player_name"]
    )

@app.route("/play", methods=["GET", "POST"])
def play():

    if "player_name" not in session:
        return redirect(url_for("set_name"))

    if "current" not in session:
        session["current"] = pick_random_phrasal_verb(verbs).__dict__

    current = PhrasalVerb(**session["current"])

    return render_template(
        "phrasal_verbs.html",
        player_name=session["player_name"],
        verb=current,
        feedback="",
        feedback_class="",
        show_next=False,
        points=session.get("points", 0),
        guesses=session.get("guesses", 0),
        accuracy=0
    )

if __name__ == "__main__":
    app.run(debug=True)