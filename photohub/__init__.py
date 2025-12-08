import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# On charge les variables d'environnement du fichier .env
load_dotenv()

app = Flask(__name__)

# Configuration de la base de données à partir des variables d'environnement
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de l'extension SQLAlchemy
db = SQLAlchemy(app)

# Importation des modèles après l'initialisation de db pour éviter les importations circulaires
from photohub import models

# Les routes et les autres composants de l'application seront importés ici
# from photohub import routes
