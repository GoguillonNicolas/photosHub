import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from photohub import app, db, bcrypt
from photohub.forms import RegistrationForm, LoginForm, AlbumForm, PhotoForm
from photohub.models import User, Album, Photo
from flask_login import login_user, current_user, logout_user, login_required

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)

    # Output resizing
    output_size = (1200, 1200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def delete_picture_file(filename):
    picture_path = os.path.join(app.root_path, 'static/uploads', filename)
    try:
        os.remove(picture_path)
    except OSError as e:
        flash(f'Error deleting file: {e}', 'danger')

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

@app.route("/album/<int:album_id>", methods=['GET', 'POST'])
@login_required
def album(album_id):
    album = Album.query.get_or_404(album_id)
    form = PhotoForm()
    if form.validate_on_submit():
        if form.photo.data:
            picture_file = save_picture(form.photo.data)
            photo = Photo(album_id=album.id, filename=picture_file, caption=form.caption.data)
            db.session.add(photo)
            db.session.commit()
            flash('Your photo has been added!', 'success')
            return redirect(url_for('album', album_id=album.id))
    return render_template('album_detail.html', title=album.title, album=album, form=form)

@app.route("/photo/<int:photo_id>/delete", methods=['POST'])
@login_required
def delete_photo(photo_id):
    photo = Photo.query.get_or_404(photo_id)
    if photo.album.owner != current_user:
        abort(403)
    album_id = photo.album.id
    delete_picture_file(photo.filename)
    db.session.delete(photo)
    db.session.commit()
    flash('Your photo has been deleted!', 'success')
    return redirect(url_for('album', album_id=album_id))

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