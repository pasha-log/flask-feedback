from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt 

db = SQLAlchemy() 

bcrypt = Bcrypt()

def connect_db(app): 
    db.app = app 
    db.init_app(app) 

class User(db.Model): 
    """User Model""" 
    """username - a unique primary key that is no longer than 20 characters.
        password - a not-nullable column that is text
        email - a not-nullable column that is unique and no longer than 50 characters.
        first_name - a not-nullable column that is no longer than 30 characters.
        last_name - a not-nullable column that is no longer than 30 characters."""

    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True) 
    password = db.Column(db.Text, nullable=False) 
    email = db.Column(db.String(50), nullable=False, unique=True) 
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback', backref='user', cascade="all,delete")

    # def __repr__(self): 
    #     u = self 
    #     return f"<User {self.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}>" 
    
    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")

        user = cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            # return user instance
            return u
        else:
            return False

class Feedback(db.Model):
    """
        id - a unique primary key that is an auto incrementing integer
        title - a not-nullable column that is at most 100 characters
        content - a not-nullable column that is text
        username - a foreign key that references the username column in the users table 
    """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    title = db.Column(db.String(100), nullable=False) 
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(20), db.ForeignKey('users.username'), nullable=False) 

    # def __repr__(self): 
    #     f = self 
    #     return f"<Feedback id={self.id} title={f.title} content={f.content} username={f.username}>" 


