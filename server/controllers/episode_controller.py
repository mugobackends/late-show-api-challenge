# server/controllers/episode_controller.py
from flask import Blueprint, jsonify, make_response
from flask_jwt_extended import jwt_required
from config import db
from models.episode import Episode
from werkzeug.exceptions import NotFound

episode_bp = Blueprint('episode_bp', __name__)

@episode_bp.route('/', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    # It's good practice to decide what level of detail to return
    # For a list, often a summary is better than full nested data
    episodes_data = [episode.to_dict() for episode in episodes]
    return make_response(jsonify(episodes_data), 200)

@episode_bp.route('/<int:id>', methods=['GET'])
def get_episode_by_id(id):
    episode = Episode.query.get(id)
    if not episode:
        raise NotFound("Episode not found")
    # Include appearances when getting a single episode
    return make_response(jsonify(episode.to_dict(include_appearances=True)), 200)

@episode_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required() # Protected route
def delete_episode(id):
    episode = Episode.query.get(id)
    if not episode:
        raise NotFound("Episode not found")

    try:
        db.session.delete(episode)
        db.session.commit()
        return make_response(jsonify({"message": "Episode and its appearances deleted successfully"}), 200)
    except Exception as e:
        db.session.rollback()
        return make_response(jsonify({"message": "Error deleting episode", "error": str(e)}), 500)