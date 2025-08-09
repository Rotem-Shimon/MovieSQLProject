import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import text
import sys


# Database connection settings
DB_NAME = 'movies_db'
DB_USER = 'postgres'
DB_PASS = '1234'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Create connection string
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Path to the data folder
data_path = 'data/ml-latest-small/'

# Load CSV files
movies = pd.read_csv(data_path + 'movies.csv')
ratings = pd.read_csv(data_path + 'ratings.csv')
tags = pd.read_csv(data_path + 'tags.csv')

# Split genres into separate rows for the genres table
genres_rows = []
for _, row in movies.iterrows():
    for genre in row['genres'].split('|'):
        genres_rows.append({'movie_id': row['movieId'], 'genre': genre})
genres = pd.DataFrame(genres_rows)

# Rename columns to match SQL table definitions
movies = movies.rename(columns={'movieId': 'movie_id', 'title': 'title', 'genres': 'ignored_genres'})
ratings = ratings.rename(columns={'userId': 'user_id', 'movieId': 'movie_id', 'rating': 'rating', 'timestamp': 'rating_time'})
tags = tags.rename(columns={'userId': 'user_id', 'movieId': 'movie_id', 'tag': 'tag', 'timestamp': 'tag_time'})

# Create dummy user data (required for gender-related analysis)
user_ids = ratings['user_id'].unique()
users = pd.DataFrame({
    'user_id': user_ids,
    'age': [25] * len(user_ids),  # Dummy age
    'gender': ['M' if i % 2 == 0 else 'F' for i in range(len(user_ids))],  # Alternate between 'M' and 'F'
    'location': ['Unknown'] * len(user_ids)  # Placeholder location
})

# Insert data into database tables
movies[['movie_id', 'title']].to_sql('movies', engine, if_exists='append', index=False)
ratings.to_sql('ratings', engine, if_exists='append', index=False)
tags.to_sql('tags', engine, if_exists='append', index=False)
genres.to_sql('genres', engine, if_exists='append', index=False)
users.to_sql('users', engine, if_exists='append', index=False)

print("✅ Data loaded successfully.")




# --- Inline Validation (runs after load; exits with code 1 on failure) ---
def _assert(cond: bool, msg: str):
    if cond:
        print(f"OK: {msg}")
    else:
        print(f"FAIL: {msg}")
        sys.exit(1)

print("🔎 Validating data integrity...")

with engine.connect() as conn:
    # 1) Row counts > 0
    for t in ["movies", "ratings", "users", "genres"]:
        n = conn.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar()
        _assert(n is not None and n > 0, f"{t} has rows (count={n})")

    # 2) Ratings within valid range [0.5, 5.0]
    min_r = conn.execute(text("SELECT MIN(rating) FROM ratings")).scalar()
    max_r = conn.execute(text("SELECT MAX(rating) FROM ratings")).scalar()
    _assert(min_r is not None and min_r >= 0.5, f"ratings min >= 0.5 (got {min_r})")
    _assert(max_r is not None and max_r <= 5.0, f"ratings max <= 5.0 (got {max_r})")

    # 3) No orphan FKs: ratings.movie_id/user_id must exist in parent tables
    orphans_movies = conn.execute(text("""
        SELECT COUNT(*) FROM ratings r
        LEFT JOIN movies m ON r.movie_id = m.movie_id
        WHERE m.movie_id IS NULL;
    """)).scalar()
    _assert(orphans_movies == 0, "ratings -> movies has no orphans")

    orphans_users = conn.execute(text("""
        SELECT COUNT(*) FROM ratings r
        LEFT JOIN users u ON r.user_id = u.user_id
        WHERE u.user_id IS NULL;
    """)).scalar()
    _assert(orphans_users == 0, "ratings -> users has no orphans")

print("✅ Validation passed.")
