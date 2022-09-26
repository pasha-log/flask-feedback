from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension 
from models import connect_db, db, User, Feedback
from forms import RegisterUserForm, LoginForm, AddFeedbackForm, DeleteForm
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.exc import IntegrityError
import os

app = Flask(__name__) 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", 'ldcnlskdcasdl0094930')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 
debug = DebugToolbarExtension(app)

connect_db(app) 
db.create_all() 

@app.route('/') 
def redirect_to_register(): 
    """Brings user to a register WTForm""" 

    return redirect("/register") 

@app.route("/register", methods=['GET', 'POST'])
def register_page():
    """Shows a form that when submitted will register/create a user.
    This form should accept a username, password, email, first_name, and last_name.
    Process the registration form by adding a new user. Then redirect to /secret""" 

    form = RegisterUserForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username, password, email, first_name, last_name)
        # db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username taken.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash(f'Welcome! You Now Have An Account, {new_user.username}!', "success")
        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():

    if "username" in session:
        return redirect(f"/users/{session['username']}")
        # return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"We've missed you, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template("login.html", form=form)

    return render_template('login.html', form=form)

@app.route('/users/<username>')
def show_user_page(username):
    """GET /users/<username>
        Displays template that shows information about that user (everything except for their password)

        Should ensure that only logged in users can access this page.
        
        Show all of the feedback that the user has given."""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    user = User.query.get(username) 
    form = DeleteForm()

    return render_template('user.html', user=user, form=form)

@app.route('/logout', methods=['GET'])
def logout_user():
    """GET /logout - Clear any information from the session and redirect to /"""
    session.clear()
    return redirect('/')

@app.route('/users/<username>/feedback/add', methods=["GET", "POST"])
def process_new_feedback(username):
    """
        GET /users/<username>/feedback/add
            Display a form to add feedback Make sure that only the user who is logged in can see this form

        POST /users/<username>/feedback/add
            Add a new piece of feedback and redirect to /users/<username> — Make sure that only the user who is logged in can successfully add feedback"""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/') 

    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        db.session.add(feedback) 
        db.session.commit()

        return redirect(f'/users/{ feedback.username }')
    else: 
        return render_template("feedback/create.html", form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=["GET", "POST"])
def edit_post(feedback_id): 
    """
        GET /feedback/<feedback_id>/update
            Displaying a form to edit feedback — **Making sure that only the user who has written that feedback can see this form **
        POST /feedback/<feedback_id>/update
            Updating a specific piece of feedback and redirect to /users/<username> — Making sure that only the user who has written that feedback can update it""" 


    feedback = Feedback.query.get(feedback_id) 
    
    if "username" not in session:
        flash("Please login first!", "danger")
        return redirect('/')

    form = AddFeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()
        return redirect(f'/users/{ feedback.username }')
    return render_template('feedback/edit.html', form=form, feedback=feedback)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""

    if "username" not in session or username != session['username']:
        flash("Please login first!", "danger")
        return redirect('/')

    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")