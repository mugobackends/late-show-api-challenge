# server/app.py
from flask import jsonify, request, make_response
from flask_restful import Api, Resource
from werkzeug.exceptions import NotFound, Unauthorized, BadRequest

from config import app, db # Import app and db from config
from models.user import User # Import your models as you create them
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance

# Import controllers
from controllers.auth_controller import auth_bp
from controllers.guest_controller import guest_bp
from controllers.episode_controller import episode_bp
from controllers.appearance_controller import appearance_bp

# Register Blueprints for organizing routes
app.register_blueprint(auth_bp, url_prefix='/') # Auth routes typically at root
app.register_blueprint(guest_bp, url_prefix='/guests')
app.register_blueprint(episode_bp, url_prefix='/episodes')
app.register_blueprint(appearance_bp, url_prefix='/appearances') # Note: Appearance POST handled via its own BP, but other appearnce GETs might be nested under episode

# Initialize Flask-RESTful API (optional, but good for structured APIs)
api = Api(app)

# --- Error Handling ---
@app.errorhandler(NotFound)
def handle_not_found(e):
    response = make_response(
        jsonify({"message": "Resource not found"}),
        404
    )
    return response

@app.errorhandler(Unauthorized)
def handle_unauthorized(e):
    response = make_response(
        jsonify({"message": "Authentication required or invalid token"}),
        401
    )
    return response

@app.errorhandler(BadRequest)
def handle_bad_request(e):
    response = make_response(
        jsonify({"message": e.description if e.description else "Bad Request"}),
        400
    )
    return response

# General error handler for unexpected errors
@app.errorhandler(Exception)
def handle_generic_exception(e):
    print(f"An unexpected error occurred: {e}") # Log the error for debugging
    response = make_response(
        jsonify({"message": "An unexpected error occurred", "error": str(e)}),
        500
    )
    return response

# --- Basic Home Route (Optional but good for testing if server is up) ---
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Late Show API!"})

if __name__ == '__main__':
    app.run(port=5555, debug=True) # Run on a specific port, enable debug mode for development