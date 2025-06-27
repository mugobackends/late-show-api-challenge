# server/models/appearance.py
from config import db
from sqlalchemy.orm import validates # For custom validation

class Appearance(db.Model):
    __tablename__ = 'appearances'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)

    # Relationships
    guest = db.relationship('Guest', back_populates='appearances')
    episode = db.relationship('Episode', back_populates='appearances')

    # Validation for rating (1-5)
    @validates('rating')
    def validate_rating(self, key, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        return rating

    def to_dict(self, include_guest=False, include_episode=False):
        data = {
            "id": self.id,
            "rating": self.rating,
            "guest_id": self.guest_id,
            "episode_id": self.episode_id
        }
        if include_guest and self.guest:
            data['guest'] = self.guest.to_dict()
        if include_episode and self.episode:
            # Avoid circular serialization if episode also includes appearances
            data['episode'] = {
                "id": self.episode.id,
                "date": self.episode.date.isoformat(),
                "number": self.episode.number
            }
        return data

    def __repr__(self):
        return f'<Appearance id={self.id} (Rating: {self.rating})>'