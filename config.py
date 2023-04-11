import os

SECRET_KEY = "felipao"

SQLALCHEMY_DATABASE_URI = \
    "{SGBD}://{user}:{password}@{server}/{database}".format(
        SGBD = "mysql+mysqlconnector",
        user = "root",
        password = "87654321",
        server = "127.0.0.1",
        database = "jogoteca"
    )
    
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + "/uploads"
