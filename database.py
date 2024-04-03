from flask_sqlalchemy import SQLAlchemy

# Instantiate the SQLAlchemy object. This will be used for all SQLAlchemy operations.
db = SQLAlchemy()

def init_app(app, database_uri=None):
    """
    Initializes the Flask application for use with the SQLAlchemy ORM.
    """
    # Configure the SQLALCHEMY_DATABASE_URI for the application.
    # This URI specifies the database type, user credentials, host, and database name.
    # A custom `database_uri` can be provided for flexibility (e.g., testing, different environments).
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri or 'postgresql://postgres:password123@localhost/atlas_joy_of_painting'
    
    # Additional configuration to avoid tracking modifications, for performance purposes.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the app with the configured database settings.
    # This makes the app ready to interact with the specified database using SQLAlchemy.
    db.init_app(app)

