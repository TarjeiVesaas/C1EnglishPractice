from flask import render_template, request, session, redirect, url_for

from gameLogic import (
    pick_random_phrasal_verb,
    check_particle,
    PhrasalVerb
)


def register_routes(app, verbs):

    @app.route("/play", methods=["GET", "POST"])
    def play():

        if "player_name" not in session:
            return redirect(url_for("set_name"))

        # First question
        if "current" not in session:
            session["current"] = pick_random_phrasal_verb(verbs).__dict__

        current = PhrasalVerb(**session["current"])

        feedback = ""
        feedback_class = ""
        show_next = False

        # ---------- Handle buttons ----------
        if request.method == "POST":

            action = request.form.get("action")

            # ---------------- Submit answer ----------------

            if action == "submit":

                guess = request.form.get("particle", "").strip()

                session["guesses"] += 1

                if check_particle(current, guess):

                    session["points"] += 1

                    feedback = (
                        f"✅ Correct!<br><br>"
                        f"<strong>{current.english}</strong>"
                    )

                    feedback_class = "correct"

                else:

                    feedback = (
                        f"❌ Incorrect.<br><br>"
                        f"The correct answer is:<br>"
                        f"<strong>{current.english}</strong>"
                    )

                    feedback_class = "incorrect"

                show_next = True

            # ---------------- Next question ----------------

            elif action == "next":

                session["current"] = pick_random_phrasal_verb(verbs).__dict__

                current = PhrasalVerb(**session["current"])

        accuracy = 0

        if session["guesses"] > 0:
            accuracy = round(
                session["points"] / session["guesses"] * 100,
                1
            )

        return render_template(
            "phrasal_verbs.html",
            player_name=session["player_name"],
            verb=current,
            feedback=feedback,
            feedback_class=feedback_class,
            show_next=show_next,
            points=session["points"],
            guesses=session["guesses"],
            accuracy=accuracy
        )