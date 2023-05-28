from flask import Flask, render_template, url_for, flash, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from stagelopen import db
from werkzeug.security import generate_password_hash,check_password_hash
from stagelopen.models import User
from stagelopen.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from stagelopen.users.picture_handler import add_profile_pic
from stagelopen.models import Stage


users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data, role = form.role.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)



@users.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@users.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
    
        user = User.query.filter_by(email = form.email.data).first()
        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            next = request.args.get('next')
            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)
    return render_template('login.html', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.dashboard'))

@users.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    role = current_user.role
    if role == "student":
        stages = Stage.query.filter_by(student_id=current_user.email)
        return render_template("student_dashboard.html", stages=stages)
    elif role == "begeleider":
        stages = Stage.query.all()
        return render_template("begeleider.html", stages=stages)
    else:
        return redirect(url_for('core.index'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():

    form = UpdateUserForm()

    if form.validate_on_submit():
        print(form)
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data,username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('User Account Updated')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename='profile_pics/' + current_user.profile_image)
    return render_template('account.html', profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username):
    
    user = User.query.filter_by(username=username).first_or_404()
    
    return render_template('user_blog_posts.html', user=user)

