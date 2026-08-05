# Retail Order Analytics — Is Any Category Quietly Struggling?

End-to-end data analytics project: messy raw data → cleaning → SQL + Python (Plotly) analysis → Power BI-ready export.

## Business Question
Total Q3 2024 revenue looks roughly flat-to-up versus Q2 at first glance. But is that number hiding a real problem in a specific category or customer segment — and if so, is it a demand issue or a supply/stockout issue?

## Key Finding
Total revenue growth (+3.4% Q2→Q3) is masking a **35–37% revenue decline in Fashion and Beauty**, offset by growth in other categories. Order *volume* for these two categories collapses in Aug–Sep while average order value stays flat — a pattern consistent with a **supply-side issue (stockouts/listing downtime)**, not weakening demand. The decline hits all customer value segments proportionally, ruling out a loyalty/churn story.

## Project Structure
```
Retail-Analytics/
├── data/
│   ├── raw_orders.csv        # original messy export (generated)
│   ├── cleaned_orders.csv    # after cleaning
│   ├── orders_powerbi.csv    # completed orders only, ready for Power BI
│   └── retail.db             # SQLite DB for SQL practice/queries
├── generate_data.py          # builds the messy dataset (documents what's "wrong" with it)
├── clean_data.py             # standalone, reusable cleaning pipeline
├── sql_analysis.sql          # SQL-only version of the core analysis
├── analysis.ipynb            # full Python interactive analysis (Plotly)
├── analysis.py               # Python source script with Plotly visualizations
├── outputs_*.png             # chart exports referenced in the notebook
├── requirements.txt          # dependencies (pandas, numpy, plotly, jupyter)
├── .gitignore                # git ignore rules for Python, Jupyter & OS metadata
└── LICENSE                   # MIT License
```

## Data Quality Issues Handled
- Mixed date formats within a single column (`YYYY-MM-DD`, `DD/MM/YYYY`, `MM-DD-YYYY`)
- Inconsistent casing/whitespace in `country`, `payment_method`, `channel`, `order_status`
- Missing `customer_id`, `unit_price`, `quantity`, `payment_method`
- Price outliers from data-entry errors (extra zeros), fixed with category-aware capping
- Exact duplicate rows

## How to Run
```bash
pip install -r requirements.txt
python generate_data.py      # (optional — raw data already included)
python clean_data.py         # produces cleaned CSV, Power BI CSV, and SQLite DB
python analysis.py           # runs Python analysis & generates Plotly charts
jupyter notebook analysis.ipynb
```
For the SQL version:
```bash
sqlite3 data/retail.db < sql_analysis.sql
```

## Power BI
Import `data/orders_powerbi.csv` directly — it's already cleaned, deduplicated, and has `month`/`quarter`/`revenue` columns ready for a category-by-quarter matrix visual or a line chart of monthly revenue split by category.

## Tools Used
Python (pandas, numpy, Plotly), SQL (SQLite), Power BI, Jupyter.

---

### Note for Reviewers
*Raw/cleaned CSV datasets (`raw_orders.csv`, `cleaned_orders.csv`, `orders_powerbi.csv`) and the SQLite database (`retail.db`) are intentionally committed directly to the `data/` folder in this repository for reviewer convenience so that the project, SQL queries, and Python notebooks can be evaluated out-of-the-box without requiring local data re-generation.*

*Note: this dataset is synthetically generated for portfolio purposes, with the Fashion/Beauty stockout pattern intentionally built in so the analysis has a clear, defensible conclusion to walk through in an interview.*
