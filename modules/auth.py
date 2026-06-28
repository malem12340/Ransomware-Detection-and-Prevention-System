from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from db import Database

auth = Blueprint("auth", __name__)


# ------------------ LOGIN ------------------
@auth.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        db = Database()

        query = "SELECT * FROM users WHERE username=%s"

        db.execute(query, (username,))

        user = db.fetchone()

        # Clear any remaining results
        db.cursor.fetchall()

        if user:

            if check_password_hash(user["password"], password):

                session["user_id"] = user["id"]
                session["username"] = user["username"]

                # Save Login Log
                log_query = """
                INSERT INTO logs(username,action)
                VALUES(%s,%s)
                """

                db.execute(log_query, (username, "Login Successful"))

                db.close()

                return redirect(url_for("dashboard"))

            else:

                flash("Invalid Password", "danger")

        else:

            flash("Username not found", "danger")

        db.close()

    return render_template("login.html")


# ------------------ LOGOUT ------------------
@auth.route("/logout")
def logout():

    username = session.get("username")

    if username:

        db = Database()

        query = """
        INSERT INTO logs(username,action)
        VALUES(%s,%s)
        """

        db.execute(query, (username, "Logout"))

        db.close()

    session.clear()

    return redirect(url_for("auth.login"))