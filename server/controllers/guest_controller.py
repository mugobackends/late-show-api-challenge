# server/controllers/guest_controller.py
from flask import Blueprint, jsonify, make_response
from config import db
from models.guest import Guest

guest_bp = Blueprint('guest_bp', __name__)

@guest_bp.route('/', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    guests_data = [guest.to_dict() for guest in guests]
    return make_response(jsonify(guests_data), 200)