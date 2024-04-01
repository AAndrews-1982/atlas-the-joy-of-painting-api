-- Create Episodes table
CREATE TABLE Episodes (
    episode_id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT
);

-- Create Colors table
CREATE TABLE Colors (
    color_id SERIAL PRIMARY KEY,
    color_name VARCHAR(50) UNIQUE NOT NULL
);

-- Create Subjects table
CREATE TABLE Subjects (
    subject_id SERIAL PRIMARY KEY,
    subject_name VARCHAR(100) UNIQUE NOT NULL
);

-- Create Broadcast Dates table
CREATE TABLE Broadcast_Dates (
    episode_id INT,
    broadcast_date DATE,
    PRIMARY KEY (episode_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id)
);

-- Create Episode_Colors join table
CREATE TABLE Episode_Colors (
    episode_id INT,
    color_id INT,
    PRIMARY KEY (episode_id, color_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
    FOREIGN KEY (color_id) REFERENCES Colors(color_id)
);

-- Create Episode_Subjects join table
CREATE TABLE Episode_Subjects (
    episode_id INT,
    subject_id INT,
    PRIMARY KEY (episode_id, subject_id),
    FOREIGN KEY (episode_id) REFERENCES Episodes(episode_id),
    FOREIGN KEY (subject_id) REFERENCES Subjects(subject_id)
);
