# 🎬 MovieLens SQL Analytics
📊 **PostgreSQL + Python + Data Visualization** project analyzing the MovieLens dataset.  
Demonstrates **SQL modeling, ETL, advanced queries, and visual insights** — clean, fast, and industry-standard.

---

## 🚀 Highlights
- 🗄 **Database Design** – Normalized schema with PK/FK integrity  
- ⚡ **ETL with Python** – Load raw CSV → PostgreSQL via SQLAlchemy  
- 📈 **Advanced SQL** – Joins, aggregations, HAVING filters, subqueries  
- 🎨 **Visualizations** – Charts + CSV reports for key metrics  

---

## 🗺 ERD
![ERD](output/ERD.png)

---

## 📊 Example Output
![Top 10 Highest Rated Movies](output/Top10HighestRatedMovies.png)

---

## 📂 Structure
```
sql/         → create_tables.sql, analysis_queries.sql
scripts/     → load_data.py, analysis.py
data/        → MovieLens CSV dataset
output/      → CSV results + charts
```

---

## 📊 Sample Insights
- 🎥 **Top Rated Movies** (min 100 ratings)  
- 📌 **Most Popular Movies** (#ratings)  
- 🎭 **Average Ratings by Genre**  
- 👫 **Gender Rating Gaps** (synthetic demo data)  

---

## 🏃 How to Run
```bash
# 1️⃣ Load dataset into PostgreSQL (with inline data validation)
python scripts/load_data.py

# 2️⃣ Create tables & schema
psql -U postgres -d movies_db -f sql/create_tables.sql

# 3️⃣ Run analysis queries & export results
python scripts/analysis.py
```
💡 All CSV outputs + charts will be generated inside `/output`

---

## 🛠 Tech Stack
**PostgreSQL**, **Python** (pandas, SQLAlchemy, matplotlib), **GitHub**