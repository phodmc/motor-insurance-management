from app import app
from flask import flash, redirect, render_template, url_for
from app.forms import LoginForm, SignupForm


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Miguel"}
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
    return render_template("index.html", user=user, vehicles=vehicles)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f"login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect("/index")
    return render_template("login.html", title="Sign In", form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash(
            f"login requested for user {form.username.data}, remember_me={form.remember_me.data}"
        )
        return redirect(url_for("index"))
    return render_template("signup.html", title="Sign Up", form=form)
