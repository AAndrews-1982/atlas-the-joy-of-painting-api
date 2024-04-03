from flask import Flask, jsonify, request
from database import db, init_app
from models import Episode, Color
from etl import run_etl

app = Flask(__name__)
init_app(app)  # Initialize the app with the database setup

@app.route('/api/episodes', methods=['GET'])
def get_episodes():
    """
    Endpoint to retrieve episodes based on filtering criteria: month, subject matter, and colors.
    Supports logical filtering with 'AND' (default) or 'OR' to combine multiple filters.
    """
    # Extract query parameters
    month = request.args.get('month')
    subject_matter = request.args.get('subject_matter')
    colors = request.args.getlist('colors')  # Allows multiple color filters
    filter_logic = request.args.get('filter_logic', default='AND')  # Default logic is 'AND'

    # Start building the query based on the Episode model
    query = Episode.query

    # Apply filters based on the query parameters received
    if month:
        # Apply month filter; supports single or multiple months for 'OR' logic
        query = apply_month_filter(query, month, filter_logic)

    if subject_matter:
        # Apply subject matter filter; supports partial match and 'OR' logic for multiple subjects
        query = apply_subject_matter_filter(query, subject_matter, filter_logic)

    if colors:
        # Apply color filter; supports filtering by multiple colors
        query = apply_color_filter(query, colors, filter_logic)

    # Execute the query
    episodes = query.all()

    # Serialize episode data for the response
    episode_data = [serialize_episode(episode) for episode in episodes]

    return jsonify(episode_data)

def apply_month_filter(query, month, logic):
    """Applies filtering based on the episode's month."""
    if logic == 'AND':
        return query.filter(Episode.month == month)
    else:
        return query.filter(Episode.month.in_(month.split(',')))

def apply_subject_matter_filter(query, subject_matter, logic):
    """Applies filtering based on the episode's subject matter."""
    if logic == 'AND':
        return query.filter(Episode.subject_matter.contains(subject_matter))
    else:
        return query.filter(Episode.subject_matter.in_(subject_matter.split(',')))

def apply_color_filter(query, colors, logic):
    """Applies filtering based on the colors used in the episode."""
    query = query.join(Color).filter(Color.name.in_(colors))
    return query.group_by(Episode.id) if logic != 'AND' else query

def serialize_episode(episode):
    """Serializes an episode object to a dictionary."""
    return {
        'id': episode.id,
        'title': episode.title,
        'month': episode.month,
        'subject_matter': episode.subject_matter,
        'colors': [color.name for color in episode.colors]
    }

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
        run_etl()  # Run the ETL process to populate the database
    app.run()  # Start the Flask application
