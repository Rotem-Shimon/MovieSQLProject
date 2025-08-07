-- 1. Average rating per movie (only for movies with at least 10 ratings)
SELECT
    m.movie_id,
    m.title,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(*) AS num_ratings
FROM
    ratings r
JOIN
    movies m ON r.movie_id = m.movie_id
GROUP BY
    m.movie_id, m.title
HAVING
    COUNT(*) >= 10
ORDER BY
    avg_rating DESC;
-- Explanation:
-- Returns average rating and number of ratings for each movie.
-- Filters out movies with fewer than 10 ratings to avoid unreliable averages.


-- 2. Top 10 most rated movies (including their average rating)
SELECT
    m.movie_id,
    m.title,
    COUNT(*) AS num_ratings,
    ROUND(AVG(r.rating), 2) AS avg_rating
FROM
    ratings r
JOIN
    movies m ON r.movie_id = m.movie_id
GROUP BY
    m.movie_id, m.title
ORDER BY
    num_ratings DESC
LIMIT 10;
-- Explanation:
-- Shows the 10 most frequently rated movies, adding average rating for comparison between popularity and quality.


-- 3. Average rating per genre (flattened genre list)
SELECT
    genre,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(*) AS num_ratings
FROM
    ratings r
JOIN
    movies m ON r.movie_id = m.movie_id,
    UNNEST(STRING_TO_ARRAY(m.genres, '|')) AS genre
GROUP BY
    genre
HAVING
    COUNT(*) >= 100
ORDER BY
    avg_rating DESC;
-- Explanation:
-- Splits genre field into individual genres using PostgreSQL's UNNEST + STRING_TO_ARRAY.
-- Averages ratings per genre and filters out genres with too few ratings.


-- 4. Top 10 most active users (by number of ratings)
SELECT
    r.user_id,
    COUNT(*) AS num_ratings
FROM
    ratings r
GROUP BY
    r.user_id
ORDER BY
    num_ratings DESC
LIMIT 10;
-- Explanation:
-- Finds users who rated the most movies, useful for identifying highly active users.


-- 5. Movies with biggest gender rating gap
SELECT
    m.movie_id,
    m.title,
    ROUND(AVG(CASE WHEN u.gender = 'M' THEN r.rating END), 2) AS avg_male,
    ROUND(AVG(CASE WHEN u.gender = 'F' THEN r.rating END), 2) AS avg_female,
    ROUND(ABS(AVG(CASE WHEN u.gender = 'M' THEN r.rating END) - AVG(CASE WHEN u.gender = 'F' THEN r.rating END)), 2) AS gender_gap,
    COUNT(*) AS num_ratings
FROM
    ratings r
JOIN
    movies m ON r.movie_id = m.movie_id
JOIN
    users u ON r.user_id = u.user_id
GROUP BY
    m.movie_id, m.title
HAVING
    COUNT(*) >= 50 AND COUNT(DISTINCT u.gender) = 2
ORDER BY
    gender_gap DESC
LIMIT 10;
-- Explanation:
-- Calculates average rating per gender per movie, then computes absolute difference.
-- Filters for movies rated by both genders and with at least 50 ratings to ensure meaningful gaps.


-- 6. Movies with highest rating standard deviation (most controversial)
SELECT
    m.movie_id,
    m.title,
    ROUND(STDDEV(r.rating), 2) AS std_dev,
    COUNT(*) AS num_ratings
FROM
    ratings r
JOIN
    movies m ON r.movie_id = m.movie_id
GROUP BY
    m.movie_id, m.title
HAVING
    COUNT(*) >= 20
ORDER BY
    std_dev DESC
LIMIT 10;
-- Explanation:
-- Measures how spread out the ratings are using STDDEV (standard deviation).
-- Helps identify divisive movies that people either love or hate.
