from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import User, Service
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from jinja2 import Template

# FLOOR PROF DATA
from .data_floorproof import code_confirm

auth = Blueprint('auth', __name__)


@auth.route('/sign_up', methods=['POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = generate_password_hash(request.form.get('password'), method='sha256')
        username = request.form.get('username')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Аккаунт уже создан', category='error')
            return redirect(url_for('auth.login'))

        else:
            session['user'] = [email, password, username]
            code_confirm(email)
            session['open_code_confirm'] = True

            return redirect(url_for("auth.email_confirm"))

        return redirect(url_for('views.home'))


@auth.route('sign_up/email_comfirm', methods=['GET', 'POST'])
def email_confirm():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    try:
        if not session['open_code_confirm']:
            return redirect(url_for('views.home'))
    except:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        input_code = request.form.get('code').lstrip().rstrip()
        if session['send_code'] == input_code:
            session['open_code_confirm'] = False
            session['open_service_confirm'] = True
            return redirect(url_for('auth.service_confirm'))
        else:
            flash('Incorect code')

    return render_template("check_code.html", login="active", user=current_user)


@auth.route('sign_up/service_comfirm', methods=['GET', 'POST'])
def service_confirm():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    try:
        if not session['open_service_confirm']:
            return redirect(url_for('views.home'))
    except:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        services_id = request.form.getlist('checkbox_service')


        # add user to database
        new_user = User(email=session['user'][0],
                        password=session['user'][1],
                        username=session['user'][2])

        for i in services_id:
            service = Service.query.filter_by(service_id=i).first()
            new_user.services.append(service)


        db.session.add(new_user)
        db.session.commit()

        login_user(new_user, remember=True)  # remember login user session

        session['open_service_confirm'] = False
        return redirect(url_for('views.profile'))

    services = Service.query.all()
    return render_template("choose_service.html", login="active", services=services, user=current_user)


# send img python outlock
# 202039@astanait.edu.kz
# Please log in to access this page.

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('views.home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True)  # remember login user session
                # session['userLogged'] = email
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try agaun.', category='error')
        else:
            print('Flask')
            flash('Email does not exist.', category='error')

    return render_template("login.html", login="active",  user=current_user)


@auth.route('/logout')
@login_required  # you can't log out if you not log in
def logout():
    session['open_code_confirm'] = False
    session['new_password_confirm'] = False
    logout_user()
    return redirect(url_for('views.home'))
