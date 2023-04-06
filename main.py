from flask import Flask, render_template, request, redirect, session, flash, url_for

class Game:
    def __init__(self, name, category, platform):
        self.name = name
        self.category = category
        self.platform = platform
        
game_1 = Game("Super Mario", "Action RPG", "Super Nintendo")
game_2 = Game("God of War", "Rack n Slash", "Playstation 2")
game_3 = Game("Mortal Kombat", "Fight", "Playstation 2")

class User:
    def __init__(self, name, nickname, password):
        self.name = name
        self.nickname = nickname
        self.password = password
        
games = [game_1, game_2, game_3]

user1 = User("Felipe Rodrigues", "fehenriq", "12345")
user2 = User("Bruno Rodrigues", "bruno_pato", "12345")
user3 = User("Nilcio Rodrigues", "nr_eletricas", "12345")

users = {user1.nickname: user1, user2.nickname: user2, user3.nickname: user3,}

app = Flask(__name__)
app.secret_key = "felipao"

@app.route("/")
def index():
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
    
    game = Game(name, category, platform)
    games.append(game)
    
    return redirect(url_for("index"))

@app.route("/login")
def login():
    next_page = request.args.get("next_page")
    return render_template("login.html", next_page=next_page)

@app.route("/authenticate", methods=["POST",])
def authenticate():
    if request.form["user"] in users:
        user = users[request.form["user"]]
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

app.run(debug=True, port=3001)
