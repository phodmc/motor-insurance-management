from urllib.parse import urlsplit
from app import app
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
import sqlalchemy as sa
from app import db
from app.models import User
from app.forms import LoginForm, SignupForm, ParticipantForm


@app.route("/")
@app.route("/index")
@login_required
def index():
    vehicles = [
        {
            "owner": {"name": "Foday Sanyang"},
            "plate": "BJL 7717 Z",
            "make": "Ford Focus RS",
        },
        {
            "owner": {"name": "Muhammed Drammeh"},
            "plate": "BJL 8976 D",
            "make": "Volvo S8",
        },
    ]
    return render_template("index.html", vehicles=vehicles)


@app.route("/login", methods=["GET", "POST"])
def login():
    # route to homepage if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        # query database for user
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )

        # login again if password or username is wrong
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))

        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)

    return render_template("login.html", title="Sign In", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]

    return render_template("user.html", user=user, posts=posts)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = SignupForm()

    if form.validate_on_submit():
        user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("User registration successful!")
        return redirect(url_for("login"))
    return render_template("signup.html", title="Sign Up", form=form)


@app.route("/participant", methods=["GET", "POST"])
@login_required
def participant():
    form = ParticipantForm()
    return render_template("create_participant.html", form=form)
