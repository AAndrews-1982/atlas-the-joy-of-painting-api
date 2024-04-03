import pandas as pd
from models import Episode, Color
from database import db

def extract_data():
    """
    Extracts data from CSV files for episodes, colors, and guests.

    Returns:
        Tuple of DataFrames: Contains data frames for episodes, colors, and guests.
    """
    # Paths to CSV files
    episodes_path = 'ColorsUsed.csv'  # Assuming a typo in the file naming; adjust as needed.
    colors_path = 'SubjectMatter.csv'  # Assuming a typo in the file naming; adjust as needed.
    guests_path = 'Episode.csv'  # Adjust path/filename as needed.

    # Read CSV files into pandas DataFrames
    episodes_df = pd.read_csv(episodes_path)
    colors_df = pd.read_csv(colors_path)
    guests_df = pd.read_csv(guests_path, on_bad_lines='skip')  # Skip bad lines

    return episodes_df, colors_df, guests_df

def transform_data(episodes_df, colors_df, guests_df):
    """
    Transforms the extracted data for consistency and usability.

    Parameters:
        episodes_df (DataFrame): Contains episodes data.
        colors_df (DataFrame): Contains colors data.
        guests_df (DataFrame): Contains guests data.

    Returns:
        Tuple of DataFrames: Transformed data frames for episodes, colors, and guests.
    """
    # Transform episodes data (Example: renaming columns for consistency)
    transformed_episodes = episodes_df.rename(columns={'EPISODE': 'title'})

    # Transform colors data (Example: dropping rows with missing color information)
    transformed_colors = colors_df.dropna()

    # Assuming transformation for guests is required; example not provided as original code does not manipulate guests_df
    transformed_guests = guests_df.copy()  # Placeholder for any transformations needed for guests

    return transformed_episodes, transformed_colors, transformed_guests

def load_data(episodes, colors, guests):
    """
    Loads the transformed data into the database using the defined models.

    Parameters:
        episodes (DataFrame): Transformed episodes data.
        colors (DataFrame): Transformed colors data.
        guests (DataFrame): Transformed guests data. (unused in the original example)
    """
    # Load episode data into the database
    for _, episode_data in episodes.iterrows():
        episode = Episode(title=episode_data['title'])
        db.session.add(episode)
    db.session.commit()  # Commit episodes to get generated IDs

    # Associate colors with episodes and load into the database
    for _, color_data in colors.iterrows():
        # Assuming each row in colors DataFrame is linked to an episode by a title or ID
        episode = Episode.query.filter_by(title=color_data['episode_title']).first()
        if episode:
            color = Color(name=color_data['COLOR'], episode_id=episode.id)
            db.session.add(color)
    db.session.commit()  # Commit colors

    # Placeholder for loading guest data, assuming similar process as above
    # ...

def run_etl():
    """
    Orchestrates the ETL process: extracting data from CSV files, transforming it,
    and loading into the database.
    """
    episodes_df, colors_df, guests_df = extract_data()
    transformed_episodes, transformed_colors, transformed_guests = transform_data(episodes_df, colors_df, guests_df)
    load_data(transformed_episodes, transformed_colors, transformed_guests)

if __name__ == "__main__":
    run_etl()
