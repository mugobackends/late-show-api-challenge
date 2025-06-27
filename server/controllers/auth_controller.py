# server/controllers/auth_controller.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from config import db, jwt
from models.user import User

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return make_response(jsonify({"message": "Username and password are required"}), 400)

    if User.query.filter_by(username=username).first():
        return make_response(jsonify({"message": "Username already exists"}), 409) # 409 Conflict

    try:
        new_user = User(username=username)
        new_user.password_hash = password # Uses the setter to hash the password
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({"message": "User registered successfully"}), 201)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Error registering user", "error": str(e)}), 500)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return make_response(jsonify({"message": "Invalid credentials"}), 401)