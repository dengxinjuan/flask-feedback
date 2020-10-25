from flask import Flask, render_template,session,redirect
from flask_debugtoolbar import DebugToolbarExtension

from models import db,connect_db, User,Feedback
from forms import LoginForm,RegisterForm,FeedbackForm

app = Flask(__name__)
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///flask-feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "youdontknowthesecretkey"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

toolbar = DebugToolbarExtension(app)

#connect app
connect_db(app)
# create table
db.create_all()


@app.route("/")
def home():
    return render_template("base.html")


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register a user: produce form and handle form submission."""

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        user = User.register(username, password, first_name, last_name, email)

        db.session.add(user)

        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)


@app.route("/login",methods=["GET","POST"])
def login_user():
    """return login user form"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username,password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Password/Username Wrong!!!"]
            return render_template("login.html",form=form)

    return render_template("login.html",form=form)

@app.route("/secret")
def show_secret():
    """enter the secret place"""
    return render_template("secret.html")


@app.route("/users/<username>")
def show_user(username):
    user = User.query.get(username)
    feedback = user.feedback
    return render_template("user.html",user=user,feedback=feedback)


@app.route("/logout")
def log_out():
    """clear session and redirect"""
    session.pop("username")
    return redirect("/login")


@app.route("/users/<username>/delete",methods=["POST"])
def delete_user(username):
    """delete user and user feedback"""
    if "username" not in session or username != session['username']:
        raise Unauthorized()
    user= User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")


# it always say get error and i dont know why
@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    form = FeedbackForm()

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    else:
        return render_template("feedback.html", form=form)


