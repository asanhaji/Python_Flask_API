from Flask_D01 import app
from Flask_D01 import db
from Controllers.user.form.login_form import LoginForm
from Controllers.user.form.register_form import RegisterForm
from flask import (Flask, flash, redirect, render_template,
                   request, session, url_for, Blueprint)
import crypt
import random, string
from hmac import compare_digest as compare_hash
import re
from Models.user_model import User, UserModel

mod_users = Blueprint('users', __name__)

@mod_users.route('/register', methods=['GET'])
def get_register_page():
    form = RegisterForm(request.form)
    return render_template("register.html", form=form, current_page = "register")

@mod_users.route('/register', methods=['POST'])
def post_register_page():
    form = RegisterForm(request.form)
    if form.validate():
        username = form.username.data
        d_filter = {"username": "'" + username + "'"}
        model = UserModel()
        user = model.getUsers(d_filter)
        if len(user) != 0:
            flash("That username is already taken, please choose another")
        else:
            username = re.escape(form.username.data)
            password = crypt.crypt(form.password.data, getsalt())
            user = User(None, username, form.email.data, password)
            model = UserModel()
            user = model.addUser(user)[0]
            if(user != None and user.username == username):
                flash("Thanks for registering!")
                session['username'] = username
                session['logged_in'] = True
                return redirect(url_for('default.index'))
            else:
                flash("Could not register, please try again")
                session.clear()
    return render_template("register.html", form=form, current_page = "register")

@mod_users.route('/logout', methods=['GET'])
def get_logout_page():
    session['logged_in'] = False
    flash('You were logged out')
    return redirect(url_for('default.index'))

@mod_users.route('/login', methods=['GET'])
def get_login_page():
    form = LoginForm(request.form)
    return render_template("login.html", form=form, current_page = "login")

@mod_users.route('/login', methods=['POST'])
def post_login_page():
    form = LoginForm(request.form)
    if form.validate():
        username = form.username.data
        password = form.password.data
        d_filter = {"username": "'" + username + "'"}
        model = UserModel()
        user = model.getUsers(d_filter)
        if len(user) != 0:
            user = user[0]
            print(user.password)
            if compare_hash(crypt.crypt(password, user.password), user.password):
                flash("Logged successfully !")
                session['username'] = username
                session['logged_in'] = True

                return redirect(url_for('default.index'))
            else:
                flash("Invalid password")
        else:
            flash("Invalid username")
    return render_template("login.html", form=form, current_page = "login")

def getsalt(chars = string.ascii_letters + string.digits):
    return random.choice(chars) + random.choice(chars)



