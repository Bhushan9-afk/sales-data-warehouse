# Sales Data Warehouse

End-to-end sales analytics pipeline: **Python ETL → PostgreSQL → dbt → Star Schema → Power BI**

## Architecture

| Layer | Technology | Description |
|-------|------------|-------------|
| Extract | Python (pandas, SQLAlchemy) | Load 3 datasets (Superstore, Online Retail, AdventureWorks) |
| Load | PostgreSQL 16 | Raw → Staging → Warehouse schemas |
| Transform | dbt Core 1.12 | 3 staging views, 5 dims, 1 fact (incremental) |
| Test | dbt tests | 34 tests (schema, RI, data quality) |
| Visualize | Power BI | Executive dashboard (1920×1080) |
| Container | Docker | dbt environment with host PostgreSQL |

## Star Schema

![ER Diagram](docs/er_diagram.md)

- **fact_sales**: 596,144 rows (3 sources)
- **dim_date**: 4,748 dates (2010–2022)
- **dim_customer**: 22,550 customers
- **dim_product**: 5,914 products
- **dim_geography**: 652 locations
- **dim_source**: 3 sources

## Quick Start

```bash
# 1. Start PostgreSQL (local or Docker)
# 2. Run ETL
cd python && python etl.py

# 3. Run dbt
cd ../dbt_project/sales_warehouse
dbt run
dbt test

# 4. Or use Docker
cd ../../
docker compose build
docker compose run dbt dbt debug
```

## Dashboard

Open `powerbi/SalesWarehouseDashboard_v1.0.pbix` in Power BI Desktop.

![Dashboard](screenshots/Sales_Data_Warehouse_Dashboard%201%20.png)

## Data Quality

- 33 tests pass, 1 warn (expected: 2,295 dates without sales)
- Zero nulls in fact keys
- Zero duplicates in dimensions
- Referential integrity enforced

## Tech Stack

Python 3.12 • PostgreSQL 16 • dbt Core 1.12 • Power BI • Docker