from flask import Flask, render_template,session,redirect
from flask_debugtoolbar import DebugToolbarExtension

from models import db,connect_db, User,Feedback
from forms import LoginForm,RegisterForm,FeedbackForm

app = Flask(__name__)


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
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username,password)

        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
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



@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


# it always say get error and i dont know why

@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

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



@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("update_feedback.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f"/users/{feedback.username}")

    

