import psycopg2
import pandas as pd
import os

# --- Database connection parameters ---
DB_NAME = "movies_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"

# --- Output folder for CSV files ---
output_dir = 'output/'
os.makedirs(output_dir, exist_ok=True)

# --- Connect to PostgreSQL database ---
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# --- Define the SQL queries (title → query string) ---
queries = {
    "1_avg_rating_per_movie": """
        SELECT
            m.movie_id,
            m.title,
            ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
            COUNT(*) AS num_ratings
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        GROUP BY m.movie_id, m.title
        HAVING COUNT(*) >= 10
        ORDER BY avg_rating DESC;
    """,
    "2_top10_most_rated_movies": """
        SELECT
            m.movie_id,
            m.title,
            COUNT(*) AS num_ratings,
            ROUND(AVG(r.rating)::numeric, 2) AS avg_rating
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        GROUP BY m.movie_id, m.title
        ORDER BY num_ratings DESC
        LIMIT 10;
    """,
    "3_avg_rating_per_genre": """
        SELECT
            g.genre,
            ROUND(AVG(r.rating)::numeric, 2) AS avg_rating,
            COUNT(*) AS num_ratings
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        JOIN genres g ON m.movie_id = g.movie_id
        GROUP BY g.genre
        HAVING COUNT(*) >= 100
        ORDER BY avg_rating DESC;
    """,
    "4_top10_active_users": """
        SELECT
            r.user_id,
            COUNT(*) AS num_ratings
        FROM ratings r
        GROUP BY r.user_id
        ORDER BY num_ratings DESC
        LIMIT 10;
    """,
    "5_gender_rating_gap": """
        SELECT
            m.movie_id,
            m.title,
            ROUND(AVG(CASE WHEN u.gender = 'M' THEN r.rating END)::numeric, 2) AS avg_male,
            ROUND(AVG(CASE WHEN u.gender = 'F' THEN r.rating END)::numeric, 2) AS avg_female,
            ROUND(ABS(
                AVG(CASE WHEN u.gender = 'M' THEN r.rating END) -
                AVG(CASE WHEN u.gender = 'F' THEN r.rating END)
            )::numeric, 2) AS gender_gap,
            COUNT(*) AS num_ratings
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        JOIN users u ON r.user_id = u.user_id
        GROUP BY m.movie_id, m.title
        HAVING COUNT(*) >= 50 AND COUNT(DISTINCT u.gender) = 2
        ORDER BY gender_gap DESC
        LIMIT 10;
    """,
    "6_highest_stddev_movies": """
        SELECT
            m.movie_id,
            m.title,
            ROUND(STDDEV(r.rating)::numeric, 2) AS std_dev,
            COUNT(*) AS num_ratings
        FROM ratings r
        JOIN movies m ON r.movie_id = m.movie_id
        GROUP BY m.movie_id, m.title
        HAVING COUNT(*) >= 20
        ORDER BY std_dev DESC
        LIMIT 10;
    """
}

# --- Run each query and export results to CSV ---
for title, query in queries.items():
    print(f"Running query: {title}")
    df = pd.read_sql_query(query, conn)
    output_path = os.path.join(output_dir, f"{title}.csv")  # <== fixed here
    df.to_csv(output_path, index=False)
    print(f"Saved results to: {output_path}")

# --- Close DB connection ---
conn.close()
