-- "1. Top 5 Funds by 5-Year Return":
SELECT
    df.scheme_name,
    fp.return_5yr_pct
FROM fact_performance fp
JOIN dim_fund df
    ON fp.amfi_code = df.amfi_code
ORDER BY fp.return_5yr_pct DESC
LIMIT 5;


-- "2. Average NAV per Month":
SELECT
    dd.year,
    dd.month,
    ROUND(AVG(fn.nav), 2) AS avg_nav
FROM fact_nav fn
JOIN dim_date dd
    ON fn.date_id = dd.date_id
GROUP BY dd.year, dd.month
ORDER BY dd.year, dd.month;

-- "3. SIP Year-wise Growth":
SELECT
    dd.year,
    ROUND(SUM(ft.amount_inr), 2) AS total_sip_amount
FROM fact_transactions ft
JOIN dim_date dd
    ON ft.date_id = dd.date_id
WHERE ft.transaction_type = 'SIP'
GROUP BY dd.year
ORDER BY dd.year;

-- "4. Transactions by State":
SELECT
    state,
    COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;

-- "5. Funds with Expense Ratio < 1%":
SELECT
    scheme_name,
    expense_ratio_pct
FROM dim_fund
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

-- "6. Top 10 Funds by 3-Year Return":
SELECT
    df.scheme_name,
    fp.return_3yr_pct
FROM fact_performance fp
JOIN dim_fund df
    ON fp.amfi_code = df.amfi_code
ORDER BY fp.return_3yr_pct DESC
LIMIT 10;

-- "7. Top 10 Funds by Sharpe Ratio":
SELECT
    df.scheme_name,
    fp.sharpe_ratio
FROM fact_performance fp
JOIN dim_fund df
    ON fp.amfi_code = df.amfi_code
ORDER BY fp.sharpe_ratio DESC
LIMIT 10;

-- "8. Total Investment by Gender":
SELECT
    gender,
    ROUND(SUM(amount_inr), 2) AS total_investment
FROM fact_transactions
GROUP BY gender;

-- "9. Transaction Count by Payment Mode":
SELECT
    payment_mode,
    COUNT(*) AS transaction_count
FROM fact_transactions
GROUP BY payment_mode
ORDER BY transaction_count DESC;

-- "10. Average 5-Year Return by Category":
SELECT
    df.category,
    ROUND(AVG(fp.return_5yr_pct), 2) AS avg_return_5yr
FROM fact_performance fp
JOIN dim_fund df
    ON fp.amfi_code = df.amfi_code
GROUP BY df.category
ORDER BY avg_return_5yr DESC;

-- "11. AUM by Fund House":
SELECT
    fund_house,
    MAX(aum_lakh_crore) AS latest_aum_lakh_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY latest_aum_lakh_crore DESC;

-- "Average Morningstar Rating by Category":
SELECT
    df.category,
    ROUND(AVG(fp.morningstar_rating), 2) AS avg_rating
FROM fact_performance fp
JOIN dim_fund df
    ON fp.amfi_code = df.amfi_code
GROUP BY df.category
ORDER BY avg_rating DESC;