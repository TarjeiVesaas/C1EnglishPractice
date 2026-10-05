from flask import render_template, request, session, redirect, url_for

from gameLogic import (
    generate_meaning_question,
    PhrasalVerb
)


def register_routes(app, verbs):

    @app.route("/play_phrasal_verb_test", methods=["GET", "POST"])
    def play_phrasal_verb_test():

        if "player_name" not in session:
            return redirect(url_for("set_name"))

        if "current" not in session:

            current, choices = generate_meaning_question(verbs)

            session["current"] = current.__dict__
            session["choices"] = choices
            session["answered"] = False

        current = PhrasalVerb(**session["current"])

        feedback = ""
        feedback_class = ""

        if request.method == "POST":

            action = request.form.get("action")

            if action == "answer":

                guess = request.form.get("choice")

                session["guesses"] += 1

                if guess == current.spanish:

                    session["points"] += 1

                    feedback = f"""
                    ✅ Correct!

                    <br><br>

                    <strong>{current.phrasal_verb}</strong>

                    """

                    feedback_class = "correct"

                else:

                    feedback = f"""
                    ❌ Incorrect.

                    <br><br>

                    <strong>{current.phrasal_verb}</strong>

                    <br>

                    means

                    <br>

                    <strong>{current.spanish}</strong>
                    """

                    feedback_class = "incorrect"

                session["answered"] = True

            elif action == "next":

                current, choices = generate_meaning_question(verbs)

                session["current"] = current.__dict__
                session["choices"] = choices
                session["answered"] = False

                current = PhrasalVerb(**session["current"])

                feedback = ""
                feedback_class = ""

        accuracy = 0

        if session["guesses"]:

            accuracy = round(
                session["points"] /
                session["guesses"] * 100,
                1
            )

        return render_template(
            "phrasal_verb_test.html",
            player_name=session["player_name"],
            verb=current,
            choices=session["choices"],
            answered=session["answered"],
            feedback=feedback,
            feedback_class=feedback_class,
            points=session["points"],
            guesses=session["guesses"],
            accuracy=accuracy
        )