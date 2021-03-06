# -*- coding: utf8 -*-
from flask import (Blueprint, render_template, redirect, url_for, flash)
from app import flask_bcrypt, db
from .forms import LoginForm, RegisterForm
from app.models import User, SystemRole, ForumRole, UserType
from flask.ext.login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__, template_folder='templates')

@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        # add code that checks whether the user is confirmed


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and flask_bcrypt.check_password_hash(user.password,
                form.password.data):
            login_user(user)
            flash('Welcome %s %s. You have logged in successfully.'
                    % (user.en_firstname, user.en_lastname))
            return redirect(url_for('main.index'))
        else:
            flash('User not found.')
    form.email.data = ''
    form.password.data = ''
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('Email has already been used.')
            return render_template('auth/register.html', form=form)
        else:
            # assign default role to all new users
            system_role = SystemRole.query.filter_by(default=True).first()
            forum_role = ForumRole.query.filter_by(default=True).first()
            if (form.email.data.endswith('mahidol.edu') or
                    form.email.data.endswith('mahidol.ac.th')):
                # check the student database to see if the email exists
                # check the staff database to see if the email exists
                # usertype = UserType.query.filter_by(name='STUDENT').one()
                pass
            else:
                user_type = UserType.query.filter_by(name='CUSTOMER').one()

            user = User(th_firstname=form.th_firstname.data,
                    th_lastname=form.th_lastname.data,
                    en_firstname=form.en_firstname.data,
                    en_lastname=form.en_lastname.data,
                    email=form.email.data,
                    password=form.password.data,
                    system_role=system_role,
                    forum_role=forum_role,
                    user_type=user_type,
                    )

            db.session.add(user)
            db.session.commit()
            flash('Registered successfully.')
            return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
