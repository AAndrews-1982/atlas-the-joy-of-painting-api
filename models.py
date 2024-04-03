from database import db

class Episode(db.Model):
    """
    Represents an episode of a show, storing details like title, month aired, and subject matter.
    Establishes a relationship with the Color model to track colors used in the episode.
    """
    # Define the table name explicitly if it differs from the class name's lowercase
    __tablename__ = 'episodes'

    # Column definitions
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each episode
    title = db.Column(db.String(100), nullable=False)  # Title of the episode, cannot be null
    month = db.Column(db.String(20))  # Month when the episode was aired
    subject_matter = db.Column(db.String(100))  # Subject matter of the episode

    # Relationship definition
    # Establishes a one-to-many relationship with the Color model
    colors = db.relationship('Color', backref='episode', lazy=True)

class Color(db.Model):
    """
    Represents a color used in an episode, including its name and a reference back to the associated episode.
    """
    __tablename__ = 'colors'

    # Column definitions
    id = db.Column(db.Integer, primary_key=True)  # Unique identifier for each color entry
    name = db.Column(db.String(50), nullable=False)  # Name of the color, cannot be null
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), nullable=False)  # Foreign key to the Episode model

    # The 'backref' in Episode.colors provides a reverse reference from Color to Episode.
