# 🎬 MovieSQLProject

Build and query a real-world movie dataset using PostgreSQL and Python.

## 📂 Project Structure
```
📁 data/ml-latest-small/    # Raw CSV files (movies, ratings, links, tags)
📁 sql/                     # Table creation script
    └── create_tables.sql
📁 scripts/                 # Python script to load data into DB
    └── load_data.py
📄 README.md                # Project overview
```

## 🛠 Tech Stack

- PostgreSQL 🐘  
- Python (pandas, psycopg2) 🐍  
- Visual Studio Code + PostgreSQL Extension 💻  

## 🚀 Workflow

1. Created database `movies_db` on PostgreSQL  
2. Ran `sql/create_tables.sql` to define schema  
3. Loaded data from CSVs using `scripts/load_data.py`  
4. Verified table data via PostgreSQL VS Code extension  

## ✅ Status

- ✔️ Database created and connected  
- ✔️ Tables created successfully  
- ✔️ CSV data fully imported  
- ✔️ GUI query results confirmed  

## 🧠 Next Steps

- Write advanced SQL queries 📊  
- Optional: add data analysis or visualizations using Python notebooks  
