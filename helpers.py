import os
from main import app
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators


class FormGame(FlaskForm):
    name = StringField("Name", 
                       [validators.DataRequired(), validators.Length(min=1, max=50)])
    category = StringField("Category", 
                           [validators.DataRequired(), validators.Length(min=1, max=40)])
    platform = StringField("Platform", 
                           [validators.DataRequired(), validators.Length(min=1, max=100)])
    save = SubmitField("Save")
    
class FormUser(FlaskForm):
    nickname = StringField("Nickname", 
                           [validators.DataRequired(), validators.Length(min=2, max=8)])
    password = PasswordField("Password", 
                             [validators.DataRequired(), validators.Length(min=4, max=100)])
    login = SubmitField("Login")

def recovery_image(id):
    for file_name in os.listdir(app.config["UPLOAD_PATH"]):
        if f"image_{id}" in file_name:
            return file_name
        
    return "default_image.jpg"

def delete_image(id):
    file = recovery_image(id)
    if file != "default_image.jpg":
        os.remove(os.path.join(app.config["UPLOAD_PATH"], file))
