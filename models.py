from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()



def connect_db(app):
    """Connect this database to provided Flask app.
    """

    db.app = app
    db.init_app(app)




class User(db.Model):
    """define user model"""

    __tablename__ = "users"

    username = db.Column(db.String(20),primary_key=True,
    nullable=False, unique=True)

    password = db.Column(db.Text, 
                         nullable=False)

    email = db.Column(db.String(50),
                         nullable=False)

    first_name = db.Column(db.String(30),
                         nullable=False)

    last_name = db.Column(db.String(30),
                         nullable=False)
    
     # start_register
    @classmethod
    def register(cls, username, pwd,first_name,last_name,email):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        user = cls(
            username = username,
            password = hashed_utf8,
            first_name = first_name,
            last_name = last_name,
            email = email
        )

        return user
    # end_register

    # start_authenticate
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False
    # end_authenticate  


class Feedback(db.Model):
    """define the feedback model"""

    ___tablename___ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String(100),nullable = False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.Text, db.ForeignKey("users.username"),nullable=False)


    

