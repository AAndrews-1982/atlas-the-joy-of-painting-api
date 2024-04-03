-- Define the structure for storing episode details
CREATE TABLE episodes (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    month VARCHAR(20),
    subject_matter VARCHAR(100)
);

-- Define the structure for storing colors used in episodes
CREATE TABLE colors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    episode_id INTEGER NOT NULL,
    FOREIGN KEY (episode_id) REFERENCES episodes(id)
);

-- Temporarily import episodes data from CSV
CREATE TEMPORARY TABLE tmp_episodes AS SELECT * FROM episodes WITH NO DATA;
\copy tmp_episodes(title, month, subject_matter) FROM 'atlas-the-joy-of-painting-api/DATA/Episodes.csv' CSV HEADER;
INSERT INTO episodes(title, month, subject_matter)
SELECT title, month, subject_matter FROM tmp_episodes
ON CONFLICT (title) DO NOTHING;
DROP TABLE tmp_episodes;

-- Temporarily import subject matter data, assuming the CSV has a direct reference (id or title) to episodes
CREATE TEMPORARY TABLE tmp_subject_matter AS SELECT * FROM episodes(subject_matter) WITH NO DATA;
\copy tmp_subject_matter(title, subject_matter) FROM 'atlas-the-joy-of-painting-api/DATA/SubjectMatter.csv' CSV HEADER;
UPDATE episodes e SET subject_matter = tmp.subject_matter
FROM tmp_subject_matter tmp WHERE e.title = tmp.title;
DROP TABLE tmp_subject_matter;

-- Temporarily import colors data from CSV
CREATE TEMPORARY TABLE tmp_colors_used AS SELECT * FROM colors WITH NO DATA;
\copy tmp_colors_used(name, episode_id) FROM 'atlas-the-joy-of-painting-api/DATA/ColorsUsed.csv' CSV HEADER;
INSERT INTO colors(name, episode_id)
SELECT name, episode_id FROM tmp_colors_used
ON CONFLICT DO NOTHING;
DROP TABLE tmp_colors_used;
