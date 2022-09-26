from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
# , TextAreaField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    """This form should accept a username, password, email, first_name, and last_name."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=8, max=55)])
    email = StringField("Email", validators=[Email(), InputRequired(message="Email is required"), Length(max=50)])
    first_name = StringField("First name", validators=[InputRequired(message="First name required"), Length(max=30)]) 
    last_name = StringField("Last name", validators=[InputRequired(message="Last name required"), Length(max=30)])

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=20)],)
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=55)],)

class AddFeedbackForm(FlaskForm): 
    """Add feedback as a user""" 
    
    title = StringField("Title", validators=[InputRequired(message="Title is required"), Length(max=100)])
    content = StringField("Content", validators=[InputRequired(message="Content required")]) 

class DeleteForm(FlaskForm): 
    """Intentionally blank."""
