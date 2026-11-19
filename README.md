# E-Commerce Sales Data Pipeline

## 1. Project Overview

This project implements an end-to-end E-Commerce Sales Data Pipeline using Python, PostgreSQL and SQL.

The pipeline generates sample e-commerce data, validates the data, loads it into a PostgreSQL staging database, transforms it into a dimensional data warehouse, and performs business analytics.

The project demonstrates core data engineering concepts, including data ingestion, data quality checks, relational database design, ETL processing, dimensional modelling, SQL analytics, automated testing and query performance analysis.

## 2. Project Objectives

- Generate and ingest e-commerce data from CSV and JSON files.
- Validate records for missing values, duplicates, invalid values and referential integrity.
- Load data into PostgreSQL staging tables.
- Prevent duplicate records during repeated loads.
- Transform staging data into a dimensional data warehouse.
- Perform business analytics using SQL.
- Test warehouse data using automated Python tests.
- Evaluate query performance using `EXPLAIN ANALYZE` and indexing.

## 3. Tools and Technologies

| Technology | Purpose |
|---|---|
| Python | Data generation, ingestion and testing |
| Pandas | Reading and processing datasets |
| PostgreSQL | Database and data warehouse |
| SQL | Data transformation and analytics |
| psycopg2 | Python-to-PostgreSQL connection |
| Git | Version control |
| GitHub | Project hosting |
| VS Code | Development environment |
| Ubuntu WSL | Linux development environment |

## 4. Project Structure

```text
ecommerce-capstone/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── docs/
│
├── logs/
│
├── sql/
│   ├── analytics/
│   │   └── 01_business_analysis.sql
│   ├── performance/
│   │   └── optimization_report.md
│   ├── staging/
│   │   └── 01_create_tables.sql
│   └── warehouse/
│       ├── 01_create_warehouse.sql
│       └── 02_load_warehouse.sql
│
├── src/
│   ├── database/
│   ├── ingestion/
│   │   ├── generate_data.py
│   │   └── load_data.py
│   └── validation/
│
├── tests/
│   └── test_warehouse.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## 5. Data Sources

The project uses five generated datasets:

| Dataset | Format | Records |
|---|---|---:|
| Customers | CSV | 100 |
| Products | JSON | 20 |
| Orders | CSV | 200 |
| Order items | CSV | 516 |
| Payments | CSV | 200 |
| **Total** | | **1,036** |

The sample data represents an e-commerce business with customers from five Nigerian cities: Lagos, Abuja, Kano, Bauchi and Port Harcourt.

The datasets are generated using Python with a fixed random seed to make the sample data reproducible.

**Implementation note:** The current implementation uses CSV and JSON files. REST API ingestion is a future enhancement.

## 6. Data Quality and Validation

The generated datasets were checked for:

- Missing values.
- Duplicate primary IDs.
- Invalid dates.
- Non-positive product prices.
- Non-positive order quantities.
- Non-positive unit prices.
- Non-positive payment amounts.
- Missing customer, order and product references.

All checks returned zero errors for the generated sample data.

No rejected records were identified in this clean sample.

## 7. PostgreSQL Staging Database

Database name: `ecommerce_db`

Five relational tables were created:

- `customers`
- `products`
- `orders`
- `order_items`
- `payments`

Primary keys and foreign key relationships were added to maintain data integrity.

The loading script uses `ON CONFLICT DO NOTHING` to prevent duplicate primary-key records during repeated loads.

### Staging record counts

| Table | Records |
|---|---:|
| customers | 100 |
| products | 20 |
| orders | 200 |
| order_items | 516 |
| payments | 200 |

## 8. Data Warehouse Design

A dimensional data warehouse was created using a star-schema approach.

### Dimension tables

- `dim_customer`: Customer details and location.
- `dim_product`: Product name and category.
- `dim_date`: Calendar attributes including year, month and quarter.

### Fact table

- `fact_sales`: Individual order-item sales records, quantities, unit prices, sales amounts and successful-payment status.

### Warehouse record counts

| Table | Records |
|---|---:|
| dim_customer | 100 |
| dim_product | 20 |
| dim_date | 140 |
| fact_sales | 516 |

The fact table contains one row per order item.

## 9. Business Analytics

Eight business questions were answered using SQL:

1. What is the total revenue from successfully paid orders?
2. What are the top five products by revenue?
3. Which customers have placed more than three orders?
4. What is the monthly revenue?
5. Who are the top three customers by spending in each city?
6. What percentage of orders were cancelled?
7. What is the cumulative monthly revenue?
8. Which customers have never placed an order?

### Key analytical results

| Metric | Result |
|---|---:|
| Successful payment revenue | 135,949.29 |
| Highest revenue product | Product 14 |
| Revenue of highest revenue product | 15,429.40 |
| Customers with more than 3 orders | 12 |
| Cancellation percentage | 26% |
| Customers who never ordered | 15 |

The revenue currency is not explicitly defined in the generated source data.

## 10. Query Performance Analysis

Query performance was evaluated using PostgreSQL `EXPLAIN ANALYZE`.

An index was created on the fact table:

```sql
CREATE INDEX idx_fact_sales_paid_date
ON fact_sales (successfully_paid, order_date);
```

### Performance comparison

| Metric | Before index | After index |
|---|---:|---:|
| Execution time | 3.518 ms | 2.163 ms |
| Planning time | 7.242 ms | 23.182 ms |
| Scan method | Sequential scan | Sequential scan |

PostgreSQL continued to use a sequential scan because the fact table contains only 516 records.

Although the observed execution time decreased, one run before and after indexing does not establish that the index caused the improvement. Repeated tests on a larger dataset would provide a more reliable comparison.

## 11. Automated Testing

Automated tests were implemented using Python's `unittest` framework.

Four tests passed:

- Customer dimension record count.
- Product dimension record count.
- Fact table record count.
- Revenue consistency between the warehouse and successful payments.

Test command:

```bash
python -m unittest discover -s tests -v
```

Result: **4 tests passed successfully.**

## 12. Running the Project

### Step 1: Clone the repository

```bash
git clone https://github.com/1jaiye/ecommerce-capstone.git
cd ecommerce-capstone
```

### Step 2: Create and activate a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Generate the sample datasets

```bash
python src/ingestion/generate_data.py
```

### Step 5: Create the staging tables

```bash
psql -d ecommerce_db -f sql/staging/01_create_tables.sql
```

### Step 6: Load the generated data

```bash
python src/ingestion/load_data.py
```

### Step 7: Run business analytics

```bash
psql -d ecommerce_db -f sql/analytics/01_business_analysis.sql
```

### Step 8: Create and populate the warehouse

```bash
psql -d ecommerce_db -f sql/warehouse/01_create_warehouse.sql
psql -d ecommerce_db -f sql/warehouse/02_load_warehouse.sql
```

### Step 9: Run automated tests

```bash
python -m unittest discover -s tests -v
```

## 13. Limitations and Future Improvements

The current project provides a working CSV/JSON-to-PostgreSQL pipeline and a populated dimensional warehouse.

Possible future improvements include:

- Integrating a REST API as an additional data source.
- Automating validation and rejected-record logging.
- Implementing a fully automated end-to-end pipeline.
- Adding more comprehensive error handling and logging.
- Creating architecture, entity relationship and star-schema diagrams.
- Performing repeated performance tests on larger datasets.
- Adding a dashboard for business intelligence reporting.

## 14. Conclusion

This project demonstrates the implementation of a foundational e-commerce data engineering pipeline.

It covers data generation, ingestion, validation, PostgreSQL staging, dimensional modelling, business analytics, automated testing and query performance evaluation.

The project provides practical experience with important data engineering tools and workflows while establishing a foundation for more advanced data pipeline development.