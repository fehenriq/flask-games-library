from flask import flash, redirect, render_template, request, session, url_for
from flask_bcrypt import check_password_hash

from helpers import FormUser
from main import app
from models import Users


@app.route("/login")
def login():
    next_page = request.args.get("next_page")
    form = FormUser()
    return render_template("login.html", next_page=next_page, form=form)

@app.route("/authenticate", methods=["POST",])
def authenticate():
    form = FormUser(request.form)
    user = Users.query.filter_by(nickname=form.nickname.data).first()
    password = check_password_hash(user.password, form.password.data)
    if user and password:
        session["logged_user"] = user.nickname
        flash(f"{user.nickname} logged successfully!")
        next_page = request.form["next_page"]
        return redirect(next_page)
    
    flash("User not logged")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session["logged_user"] = None
    flash("Logout successfully")
    return redirect(url_for("index"))
