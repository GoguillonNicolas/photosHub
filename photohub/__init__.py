import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
# Configurations de l'application
# Pour un projet de développement, une clé statique est acceptable.
app.config['SECRET_KEY'] = 'my-secret-key-for-dev'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions Flask
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Redirige les utilisateurs non connectés vers la page de login
login_manager.login_message_category = 'info'

# Le user_loader doit être défini avant l'importation des routes
# car les routes utilisent des décorateurs qui en dépendent.
from photohub.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Importer les routes à la fin pour éviter les dépendances circulaires.
# Le fichier routes.py a besoin d'importer 'app', qui est défini dans ce fichier.
from photohub import routes
