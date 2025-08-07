-- Create table for storing movie information
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS links;


CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,       -- Unique ID for each movie
    title VARCHAR(255),                -- Movie title
    release_year INT,                  -- Year the movie was released
    genres TEXT                        -- Pipe-separated list of genres (e.g. Comedy|Drama)
);


-- Create table for storing user information
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,        -- Unique ID for each user
    age INT CHECK (age > 0),           -- User age, must be positive
    gender VARCHAR(10),                -- User gender (e.g., 'M', 'F')
    location VARCHAR(100)              -- User location (city, country, etc.)
);

-- Create table for storing user ratings of movies
CREATE TABLE ratings (
    user_id INT REFERENCES users(user_id),      -- Link to the user who gave the rating
    movie_id INT REFERENCES movies(movie_id),   -- Link to the rated movie
    rating FLOAT CHECK (rating >= 0 AND rating <= 5),  -- Rating value between 0 and 5
    rating_time TIMESTAMP,                      -- When the rating was given
    PRIMARY KEY (user_id, movie_id)             -- Each user can rate each movie only once
);

-- Create table for assigning genres to movies
CREATE TABLE genres (
    movie_id INT REFERENCES movies(movie_id),   -- Movie that has this genre
    genre VARCHAR(50),                          -- Genre name (e.g., 'Action', 'Drama')
    PRIMARY KEY (movie_id, genre)               -- Combination must be unique
);

-- Create table for storing user-added tags on movies
CREATE TABLE tags (
    user_id INT REFERENCES users(user_id),      -- Who added the tag
    movie_id INT REFERENCES movies(movie_id),   -- Which movie was tagged
    tag TEXT,                                   -- The tag itself (free text)
    tag_time TIMESTAMP                          -- When the tag was added
);
