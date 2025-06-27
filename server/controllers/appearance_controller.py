# server/controllers/appearance_controller.py
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required
from config import db
from models.appearance import Appearance
from models.guest import Guest
from models.episode import Episode
from werkzeug.exceptions import BadRequest, NotFound

appearance_bp = Blueprint('appearance_bp', __name__)

@appearance_bp.route('/', methods=['POST'])
@jwt_required() # Protected route
def create_appearance():
    data = request.get_json()
    rating = data.get('rating')
    guest_id = data.get('guest_id')
    episode_id = data.get('episode_id')

    if not all([rating, guest_id, episode_id]):
        raise BadRequest("Rating, guest_id, and episode_id are required.")

    guest = Guest.query.get(guest_id)
    episode = Episode.query.get(episode_id)

    if not guest:
        raise NotFound("Guest not found.")
    if not episode:
        raise NotFound("Episode not found.")

    try:
        # The validation for rating (1-5) is handled by the @validates decorator in the model
        new_appearance = Appearance(
            rating=rating,
            guest=guest,    # Assigning objects directly
            episode=episode # Assigning objects directly
        )
        db.session.add(new_appearance)
        db.session.commit()
        return make_response(jsonify(new_appearance.to_dict()), 201)
    except ValueError as e: # Catch validation errors from the model
        db.session.rollback()
        raise BadRequest(str(e)) # Return as a 400 Bad Request
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Error creating appearance", "error": str(e)}), 500)

# Note: No GET /appearances route specified in the challenge,
# but individual appearances are included in episode details.