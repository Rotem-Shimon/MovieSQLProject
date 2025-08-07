# 🎬 MovieSQLProject

Build and query a real-world movie dataset using PostgreSQL and Python.

## 📂 Project Structure
📁 data/ml-latest-small/    # Raw CSV files (movies, ratings, links, tags)  
📁 output/                  # Query results (CSV files)  
📁 sql/                     # SQL scripts  
    ├── create_tables.sql   # Schema definition  
    └── analysis_queries.sql # All SQL analysis queries  
📁 scripts/                 # Python scripts  
    ├── load_data.py        # Load CSV data into PostgreSQL  
    └── analysis.py         # Run SQL queries and export results  
📄 README.md                # Project overview  

## 🛠 Tech Stack
- PostgreSQL 🐘  
- Python (pandas, psycopg2) 🐍  
- Visual Studio Code + PostgreSQL Extension 💻  

## 🚀 Workflow
1. Created database `movies_db` on PostgreSQL  
2. Ran `create_tables.sql` to define schema  
3. Loaded CSV data using `load_data.py`  
4. Created query set in `analysis_queries.sql`  
5. Ran `analysis.py` to export query results to CSV in `/output`  

## ✅ Current Progress
- ✔️ Tables and schema created  
- ✔️ All CSVs loaded into PostgreSQL  
- ✔️ Query automation working — CSVs generated  
- ✔️ Dummy `users` table added to enable gender-based analysis  

## 🧠 Next Steps
- Add visualizations using `matplotlib` / `seaborn`  
- Add more SQL queries (e.g., by year, decade, genre patterns)  
- Improve schema (e.g., normalize titles / extract year)  
- Build dashboard or use Jupyter Notebook for analysis  
- Add tests and documentation for reproducibility  

---

✔️ *Overcame challenge: manually generated dummy user data with gender info to enable `gender_rating_gap` query.*
