from flask import Flask, request, session, redirect, url_for, render_template
from phrasal_verbs import register_routes as register_phrasal_verbs
from phrasal_verb_test import register_routes as register_phrasal_verb_test
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
register_phrasal_verbs(app, verbs)
register_phrasal_verb_test(app, verbs)
current = pick_random_phrasal_verb(verbs)

@app.route("/")
def index():
    return redirect(url_for("set_name"))

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
            return redirect(url_for("play_phrasal_verbs"))

        elif game_type == "phrasal_verb_test":

            session["game_type"] = game_type
            return redirect(url_for("play_phrasal_verb_test"))

    return render_template(
        "select_game.html",
        player_name=session["player_name"]
    )

@app.route("/reset")
def reset():

    session.clear()

    return redirect(url_for("set_name"))

if __name__ == "__main__":
    app.run(debug=True)