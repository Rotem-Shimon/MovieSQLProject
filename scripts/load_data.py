import pandas as pd
from sqlalchemy import create_engine

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
