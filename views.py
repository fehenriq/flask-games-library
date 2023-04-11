from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from main import app, db
from models import Games, Users

@app.route("/")
def index():
    games = Games.query.order_by(Games.id)
    return render_template("list.html", titulo="Games", games=games)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for("login", next_page=url_for("new")))
    return render_template('new.html', titulo='New Game')

@app.route("/create", methods=["POST",])
def create():
    name = request.form["name"]
    category = request.form["category"]
    platform = request.form["platform"]
    
    game = Games.query.filter_by(name=name).first()
    
    if game:
        flash("Game already exists")
        return redirect(url_for("index"))
    
    new_game = Games(name=name, category=category, platform=platform)
    db.session.add(new_game)
    db.session.commit()
    
    file = request.files["file"]
    upload_path = app.config["UPLOAD_PATH"]
    file.save(f"{upload_path}/image_{new_game.id}.jpg")
    
    return redirect(url_for("index"))

@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for("login", next_page=url_for("edit")))
    
    game = Games.query.filter_by(id=id).first()
    return render_template('edit.html', titulo='Edit Game', game=game)

@app.route("/update", methods=["POST",])
def update():
    game = Games.query.filter_by(id=request.form["id"]).first()
    game.name = request.form["name"]
    game.category = request.form["category"]
    game.platform = request.form["platform"]
    
    db.session.add(game)
    db.session.commit()
    
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for("login"))
    
    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Game deleted successfully")
    
    return redirect(url_for("index"))

@app.route("/login")
def login():
    next_page = request.args.get("next_page")
    return render_template("login.html", next_page=next_page)

@app.route("/authenticate", methods=["POST",])
def authenticate():
    user = Users.query.filter_by(nickname=request.form["user"]).first()
    if user:
        if request.form["password"] == user.password:
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

@app.route("/uploads/<file_name>")
def image(file_name):
    return send_from_directory("uploads", file_name)