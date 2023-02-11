from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import EqualTo

class LoginForm(FlaskForm):
    username =  StringField(label='User name')
    password = PasswordField(label="Password")
    submit = SubmitField(label="Login")    

class RegisterForm(FlaskForm):
    username = StringField(label='username')
    email =  StringField(label='email')
    password1 = PasswordField(label='password1')
    password2 = PasswordField(label='password2',validators=[EqualTo('password1')])
    submit = SubmitField(label='submit')



class AdminLoginForm(FlaskForm):
    username =  StringField(label='Username')
    password = PasswordField(label="Password")
    submit = SubmitField(label="Login")    



class CategoryForm(FlaskForm):
    category_name =  StringField(label="Category_name")
    submit = SubmitField(label="Submit")    




