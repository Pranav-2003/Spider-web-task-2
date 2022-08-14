from datetime import datetime
from imp import reload
import random, string
from flask import render_template, url_for, flash, redirect, request, abort
from santa import app, db, bcrypt
from santa.forms import LoginForm, RegistrationForm, GroupForm, JoinForm, UpdateForm
from santa.models import User, Group, Members
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/", methods=['GET', 'POST'])
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password')
    return render_template('login.html', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, age=form.age.data, city=form.city.data, state=form.state.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    members = Members.query.filter_by(uid=current_user.id)
    return render_template('home.html', members=members)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/create", methods=['GET', 'POST'])
@login_required
def create():
    c = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    form = GroupForm()
    if form.validate_on_submit():
        grp = Group(name=form.name.data,id=current_user.id,code=c,date=form.date.data,budget=form.budget.data,location=form.location.data)
        db.session.add(grp)
        db.session.commit()
        n = Group.query.filter_by(code=c).first()
        u = Members(gno=n.sno,gname=form.name.data,uid=current_user.id,name=current_user.username)
        db.session.add(u)
        db.session.commit()
        flash('Your Exchange Group has been created!')
        return redirect(url_for('home'))
    return render_template('create.html', form=form)

@app.route("/join", methods=['GET', 'POST'])
@login_required
def join():
    form = JoinForm()
    if form.validate_on_submit():
        grp = Group.query.filter_by(code=form.searched.data).first()
        if grp:
            mem = Members(gno=grp.sno,gname=grp.name,uid=current_user.id,name=current_user.username)
            db.session.add(mem)
            db.session.commit()
            flash("You have been added to the group successfully!")
            return redirect(url_for('home'))
    return render_template('join.html', form=form)

@app.route("/view/<int:id>", methods=['GET', 'POST'])
@login_required
def view(id):
    details = Group.query.filter_by(sno=id).first()
    m = Members.query.filter_by(gno=id)
    return render_template('view.html', info=details, members=m)

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.email = form.email.data
        current_user.city = form.city.data
        current_user.state = form.state.data
        current_user.age = form.age.data        
        db.session.commit()
        flash('Your profile has been updated')
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.city.data = current_user.city
        form.state.data = current_user.state
        form.age.data = current_user.age
    return render_template('profile.html', form=form)
