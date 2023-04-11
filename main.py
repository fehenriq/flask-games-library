from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from views_game import *
from views_user import *

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)
csrf = CSRFProtect(app)
bcrypt = Bcrypt(app)

if __name__ == "__main__":
    app.run(debug=True, port=3001)
