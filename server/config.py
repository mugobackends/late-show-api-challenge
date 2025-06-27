# server/config.py
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

app = Flask(__name__)

# --- Database Configuration ---
# Set your PostgreSQL connection string here.
# Replace <user> and <password> with your actual PostgreSQL username and password.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://<user>:<password>@localhost:5432/late_show_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Suppresses a warning

# --- JWT Configuration ---
# IMPORTANT: Use a strong, random key in a production environment via an environment variable.
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "your_super_secret_jwt_key_here")
app.config["JWT_TOKEN_LOCATION"] = ["headers"] # Tokens are expected in the Authorization header

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)