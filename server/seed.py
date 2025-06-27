# server/seed.py
from config import app, db
from models.user import User
from models.guest import Guest
from models.episode import Episode
from models.appearance import Appearance
from werkzeug.security import generate_password_hash # Import for hashing user password
from datetime import date # For episode dates

with app.app_context():
    print("Clearing existing data...")
    Appearance.query.delete()
    Guest.query.delete()
    Episode.query.delete()
    User.query.delete()
    db.session.commit()
    print("Data cleared!")

    print("Seeding users...")
    user1 = User(username='testuser')
    user1.password_hash = 'password123' # This will call the setter and hash it
    user2 = User(username='admin')
    user2.password_hash = 'adminpass'
    db.session.add_all([user1, user2])
    db.session.commit()
    print("Users seeded!")

    print("Seeding guests...")
    guest1 = Guest(name='Jerry Seinfeld', occupation='Comedian')
    guest2 = Guest(name='Oprah Winfrey', occupation='TV Host')
    guest3 = Guest(name='Elon Musk', occupation='Entrepreneur')
    guest4 = Guest(name='Taylor Swift', occupation='Musician')
    db.session.add_all([guest1, guest2, guest3, guest4])
    db.session.commit()
    print("Guests seeded!")

    print("Seeding episodes...")
    episode1 = Episode(date=date(2024, 1, 15), number=1001)
    episode2 = Episode(date=date(2024, 2, 20), number=1002)
    episode3 = Episode(date=date(2024, 3, 5), number=1003)
    db.session.add_all([episode1, episode2, episode3])
    db.session.commit()
    print("Episodes seeded!")

    print("Seeding appearances...")
    appearance1 = Appearance(guest=guest1, episode=episode1, rating=5)
    appearance2 = Appearance(guest=guest2, episode=episode1, rating=4)
    appearance3 = Appearance(guest=guest3, episode=episode2, rating=3)
    appearance4 = Appearance(guest=guest4, episode=episode3, rating=5)
    appearance5 = Appearance(guest=guest1, episode=episode3, rating=4) # Seinfeld on another episode
    db.session.add_all([appearance1, appearance2, appearance3, appearance4, appearance5])
    db.session.commit()
    print("Appearances seeded!")

    print("Database seeding complete!")