## 📊 Portfolio & Analysis

View the complete project analysis with visualizations:

📥 [Download Portfolio PDF](Retail Analysis Report.pdf) | [View on GitHub](#)

### Key Finding
Discovered a **hidden 35-37% revenue decline** in Fashion & Beauty categories 
masked by +3.4% overall growth. Full analysis includes:
- 3 interactive visualizations (monthly trends, segment breakdown, category heatmap)
- SQL & Python analysis methodology
- Business impact assessment & recommendations

[View Full Portfolio PDF →](Retail Analysis Report.pdf)
Retail Order Analytics — Is Any Category Quietly Struggling?

End-to-end data analytics project: messy raw data → Python ETL cleaning → SQL queries → **Power BI Interactive Dashboard**.

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
│   ├── orders_powerbi.csv    # completed orders only, ready for Power BI import
│   └── retail.db             # SQLite DB for SQL practice/queries
├── generate_data.py          # builds the messy dataset (documents data quality issues)
├── clean_data.py             # standalone, reusable cleaning pipeline
├── sql_analysis.sql          # SQL-only version of the core analysis queries
├── analysis.ipynb            # Python EDA & cleaning validation notebook
├── analysis.py               # Python source script
├── requirements.txt          # dependencies (pandas, numpy, jupyter)
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

### 1. Python Data Pipeline & Cleaning
```bash
pip install -r requirements.txt
python generate_data.py      # (optional — raw data already included)
python clean_data.py         # produces cleaned CSV, Power BI CSV, and SQLite DB
python analysis.py           # runs data validation & tabular summaries
```

### 2. SQL Analysis (SQLite)
```bash
sqlite3 data/retail.db < sql_analysis.sql
```

---

## 📊 Power BI Dashboard Setup & DAX Measures

Import `data/orders_powerbi.csv` into Power BI Desktop. The dataset is pre-cleaned and deduplicated with calculated fields (`revenue`, `month`, `quarter`, `year`).

### Recommended DAX Measures

```dax
// 1. Total Revenue
Total Revenue = SUM(orders_powerbi[revenue])

// 2. Q2 Revenue
Q2 Revenue = CALCULATE([Total Revenue], orders_powerbi[quarter] = 2)

// 3. Q3 Revenue
Q3 Revenue = CALCULATE([Total Revenue], orders_powerbi[quarter] = 3)

// 4. Q2 vs Q3 Revenue Change %
Q2_to_Q3_Change_% = 
DIVIDE([Q3 Revenue] - [Q2 Revenue], [Q2 Revenue], 0)

// 5. Total Order Count
Total Orders = COUNTROWS(orders_powerbi)

// 6. Average Order Value (AOV)
Average Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

### Key Dashboard Visuals to Build
1. **Executive KPI Cards**: `Total Revenue ($)`, `Total Orders`, `Average Order Value`, `Q2 vs Q3 Growth %`.
2. **Monthly Revenue Trend (Line Chart)**: Axis = `month`, Values = `[Total Revenue]`. Highlights flat headline growth.
3. **Category Revenue Change (Clustered Column Chart)**: Axis = `category`, Values = `[Q2_to_Q3_Change_%]`. Color alert rule for negative growth (Fashion & Beauty drop).
4. **Order Volume vs AOV Diagnostic (Dual-Axis Line Chart)**: Axis = `month`, Legend = `category` (Filtered to Fashion & Beauty), Values = `[Total Orders]` and `[Average Order Value]`.
5. **Interactive Slicers**: Filter by `country`, `payment_method`, `channel`.

---

## Tools Used
Python (pandas, numpy), SQL (SQLite), Power BI, Jupyter.

---

### Note for Reviewers
*Raw/cleaned CSV datasets (`raw_orders.csv`, `cleaned_orders.csv`, `orders_powerbi.csv`) and the SQLite database (`retail.db`) are intentionally committed directly to the `data/` folder in this repository for reviewer convenience so that the project, SQL queries, and Power BI imports can be evaluated out-of-the-box without requiring local data re-generation.*

*Note: this dataset is synthetically generated for portfolio purposes, with the Fashion/Beauty stockout pattern intentionally built in so the analysis has a clear, defensible conclusion to walk through in an interview.*
