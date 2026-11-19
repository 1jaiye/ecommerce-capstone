# Query Performance Optimization Report

## Test query
Calculate daily revenue from successfully paid sales between
January 1 and June 30, 2026.

## Baseline: Before index
- Execution time: 3.518 ms
- Planning time: 7.242 ms
- Scan method: Sequential scan
- Rows returned: 52

## After creating an index
Index created:
CREATE INDEX idx_fact_sales_paid_date
ON fact_sales (successfully_paid, order_date);

- Execution time: 2.163 ms
- Planning time: 23.182 ms
- Scan method: Sequential scan
- Rows returned: 52

## Analysis
Execution time decreased by approximately 38.5% in the
observed runs. However, PostgreSQL continued to use a
sequential scan rather than the new index because the
fact_sales table contains only 516 rows.

The timing difference is not sufficient to establish that
the index caused the improvement. More repeated tests on
a larger dataset would be needed for a reliable conclusion.

## Conclusion
The index was successfully created, but PostgreSQL's
query planner determined that a sequential scan remained
appropriate for this small dataset.
