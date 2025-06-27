# server/models/episode.py
from config import db
from sqlalchemy.ext.associationproxy import association_proxy # For easier access to guests via appearances

class Episode(db.Model):
    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    number = db.Column(db.Integer, unique=True, nullable=False)

    # Relationship to Appearance, with cascade delete
    appearances = db.relationship('Appearance', back_populates='episode', cascade='all, delete-orphan')

    # Association proxy to easily access guests through appearances
    guests = association_proxy('appearances', 'guest')

    def to_dict(self, include_appearances=False):
        data = {
            "id": self.id,
            "date": self.date.isoformat(), # Format date for JSON
            "number": self.number
        }
        if include_appearances:
            data['appearances'] = [app.to_dict(include_guest=True) for app in self.appearances]
        return data

    def __repr__(self):
        return f'<Episode {self.number} on {self.date}>'