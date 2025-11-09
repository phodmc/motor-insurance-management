from random import choice

import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app import db
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class SignupForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError(
                f"username '{user.username}' already exist. Try a different one"
            )

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError(
                f"email '{user.email}' already exists. Try a different one"
            )


class ParticipantForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    gender = SelectField("Gender", choices=[("MALE", "Male"), ("FEMALE", "Female")])
    age = IntegerField("Age", validators=[DataRequired()])
    phone = StringField("Phone", validators=[DataRequired()])
    address = TextAreaField("Address", validators=[DataRequired()])
    nationality = StringField("Nationality", validators=[DataRequired()])
    occupation = StringField(
        "Occupation",
    )
    submit = SubmitField("Create Participant")


# class VehicleForm(FlaskForm):

# class PolicyForm(FlaskForm):
