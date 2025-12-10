from flask import render_template, url_for, flash, redirect, request
from photohub import app, db, bcrypt
from photohub.forms import RegistrationForm, LoginForm, AlbumForm
from photohub.models import User, Album
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home')

@app.route("/albums")
@login_required
def albums():
    user_albums = Album.query.filter_by(owner=current_user).all()
    return render_template('albums.html', title='My Albums', albums=user_albums)

@app.route("/album/new", methods=['GET', 'POST'])
@login_required
def new_album():
    form = AlbumForm()
    if form.validate_on_submit():
        album = Album(title=form.title.data, description=form.description.data, owner=current_user)
        db.session.add(album)
        db.session.commit()
        flash('Your album has been created!', 'success')
        return redirect(url_for('albums'))
    return render_template('create_album.html', title='New Album', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))