from datetime import datetime
from . import db

# Table d'association pour le partage d'albums (Many-to-Many)
album_shares = db.Table('album_shares',
    db.Column('album_id', db.Integer, db.ForeignKey('albums.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('shared_at', db.DateTime, default=datetime.utcnow)
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    owned_albums = db.relationship('Album', backref='owner', lazy=True, foreign_keys='Album.owner_id')
    comments = db.relationship('Comment', backref='author', lazy=True)
    
    # Relation pour les albums partagés avec cet utilisateur
    shared_with_me = db.relationship('Album', secondary=album_shares, lazy='subquery',
                                     backref=db.backref('shared_with_users', lazy=True))

    def __repr__(self):
        return f'<User {self.username}>'

class Album(db.Model):
    __tablename__ = 'albums'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    photos = db.relationship('Photo', backref='album', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Album {self.title}>'

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    comments = db.relationship('Comment', backref='photo', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<Photo {self.filename}>'

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Comment {self.id}>'
