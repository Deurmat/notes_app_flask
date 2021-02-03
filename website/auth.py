from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint(' auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template("login.html", boolean=True)


@auth.route('/logout')
def logout():
    return "<h1>Logout</h1>"


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email length must be greater than 3 characters', category='error')
        elif len(first_name) < 2:
            flash('Name length must be greater than 1 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters', category='error')
        else:
            # add user to database
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            flash('Account created', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html")
