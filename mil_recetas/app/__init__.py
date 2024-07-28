from flask import Flask, g
import mysql.connector
from dotenv import load_dotenv
import os
from config import bcrypt
from flask_login import LoginManager

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bebebeto11141923'
login_manager = LoginManager()
login_manager.init_app(app)

DATABASE_CONFIG = {
    'user': os.getenv('DB_USERNAME'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'port': os.getenv('DB_PORT', 3306)
}

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(**DATABASE_CONFIG)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.teardown_appcontext(close_db)

app.config['CARPETA_SUBIDA'] = 'uploads/recetas'

bcrypt.init_app(app)

from app import views

from app.models import Usuario

@login_manager.user_loader
def load_user(user_id):
    user_data = Usuario.mostrar_usuario_con_password(user_id)
    if user_data:
        return Usuario(**user_data.__dict__)
    return None