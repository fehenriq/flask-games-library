from flask import (flash, redirect, render_template, request, send_from_directory, session, url_for)
from main import app, db
from models import Games
from helpers import FormGame, delete_image, recovery_image
import time

@app.route("/")
def index():
    games = Games.query.order_by(Games.id)
    return render_template("list.html", titulo="Games", games=games)

@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for("login", next_page=url_for("new")))
    
    form = FormGame()
    return render_template('new.html', titulo='New Game', form=form)

@app.route("/create", methods=["POST",])
def create():
    form = FormGame(request.form)
    
    if not form.validate_on_submit():
        return redirect(url_for("new"))
    
    name = form.name.data
    category = form.category.data
    platform = form.platform.data
    
    game = Games.query.filter_by(name=name).first()
    
    if game:
        flash("Game already exists")
        return redirect(url_for("index"))
    
    new_game = Games(name=name, category=category, platform=platform)
    db.session.add(new_game)
    db.session.commit()
    
    file = request.files["file"]
    upload_path = app.config["UPLOAD_PATH"]
    timestamp = time.time()
    file.save(f"{upload_path}/image_{new_game.id}_{timestamp}.jpg")
    
    return redirect(url_for("index"))

@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for("login", next_page=url_for("edit")))
    
    game = Games.query.filter_by(id=id).first()
    form = FormGame()
    form.name.data = game.name
    form.category.data = game.category
    form.platform.data = game.platform
    thumbnail = recovery_image(id)
    return render_template('edit.html', titulo='Edit Game', id=id, thumbnail=thumbnail, form=form)

@app.route("/update", methods=["POST",])
def update():
    form = FormGame(request.form)
    
    if form.validate_on_submit():
        game = Games.query.filter_by(id=request.form["id"]).first()
        game.name = form.name.data
        game.category = form.category.data
        game.platform = form.platform.data
        
        db.session.add(game)
        db.session.commit()
        
        file = request.files["file"]
        upload_path = app.config["UPLOAD_PATH"]
        timestamp = time.time()
        delete_image(game.id)
        file.save(f"{upload_path}/image_{game.id}_{timestamp}.jpg")
    
    return redirect(url_for("index"))

@app.route("/delete/<int:id>")
def delete(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        return redirect(url_for("login"))
    
    Games.query.filter_by(id=id).delete()
    db.session.commit()
    flash("Game deleted successfully")
    
    return redirect(url_for("index"))

@app.route("/uploads/<file_name>")
def image(file_name):
    return send_from_directory("uploads", file_name)
