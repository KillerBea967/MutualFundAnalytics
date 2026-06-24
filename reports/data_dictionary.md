# Mutual Fund Analytics Data Dictionary - SQL


# dim_fund

| Column | Data Type | Business Definition | Source |
|----------|-----------|-------------------|--------|
| amfi_code | INTEGER | Unique AMFI code identifying a scheme | fund_master_cleaned.csv |
| scheme_name | TEXT | Name of mutual fund scheme | fund_master_cleaned.csv |
| fund_house | TEXT | Asset management company | fund_master_cleaned.csv |
| category | TEXT | Broad fund category | fund_master_cleaned.csv |
| sub_category | TEXT | Detailed fund category | fund_master_cleaned.csv |
| plan | TEXT | Direct or Regular plan | fund_master_cleaned.csv |
| fund_manager | TEXT | Fund manager name | fund_master_cleaned.csv |
| risk_category | TEXT | Risk classification | fund_master_cleaned.csv |

---

# fact_nav

| Column | Data Type | Business Definition | Source |
|----------|-----------|-------------------|--------|
| amfi_code | INTEGER | Mutual fund identifier | nav_history_cleaned.csv |
| date | DATE | NAV date | nav_history_cleaned.csv |
| nav | REAL | Net Asset Value | nav_history_cleaned.csv |

---

# fact_transactions

| Column | Data Type | Business Definition | Source |
|----------|-----------|-------------------|--------|
| investor_id | INTEGER | Unique investor identifier | investor_transactions_cleaned.csv |
| transaction_date | DATE | Date of transaction | investor_transactions_cleaned.csv |
| amfi_code | INTEGER | Scheme identifier | investor_transactions_cleaned.csv |
| transaction_type | TEXT | SIP/Lumpsum/Redemption | investor_transactions_cleaned.csv |
| amount_inr | REAL | Transaction amount in INR | investor_transactions_cleaned.csv |
| state | TEXT | Investor state | investor_transactions_cleaned.csv |
| city | TEXT | Investor city | investor_transactions_cleaned.csv |
| city_tier | TEXT | Tier classification | investor_transactions_cleaned.csv |
| age_group | TEXT | Investor age bracket | investor_transactions_cleaned.csv |
| gender | TEXT | Investor gender | investor_transactions_cleaned.csv |
| annual_income_lakh | REAL | Annual income in lakhs | investor_transactions_cleaned.csv |
| payment_mode | TEXT | Payment method | investor_transactions_cleaned.csv |
| kyc_status | TEXT | KYC verification status | investor_transactions_cleaned.csv |

---

# fact_performance

| Column | Data Type | Business Definition | Source |
|----------|-----------|-------------------|--------|
| amfi_code | INTEGER | Scheme identifier | scheme_performance_cleaned.csv |
| return_1yr_pct | REAL | 1-year return percentage | scheme_performance_cleaned.csv |
| return_3yr_pct | REAL | 3-year return percentage | scheme_performance_cleaned.csv |
| return_5yr_pct | REAL | 5-year return percentage | scheme_performance_cleaned.csv |
| benchmark_3yr_pct | REAL | Benchmark 3-year return | scheme_performance_cleaned.csv |
| alpha | REAL | Excess return over benchmark | scheme_performance_cleaned.csv |
| beta | REAL | Volatility relative to market | scheme_performance_cleaned.csv |
| sharpe_ratio | REAL | Risk-adjusted return metric | scheme_performance_cleaned.csv |
| sortino_ratio | REAL | Downside-risk-adjusted return | scheme_performance_cleaned.csv |
| std_dev_ann_pct | REAL | Annualized standard deviation | scheme_performance_cleaned.csv |
| max_drawdown_pct | REAL | Maximum decline from peak | scheme_performance_cleaned.csv |
| aum_crore | REAL | Assets under management (crores) | scheme_performance_cleaned.csv |
| expense_ratio_pct | REAL | Annual fund expense ratio | scheme_performance_cleaned.csv |
| morningstar_rating | INTEGER | Morningstar rating | scheme_performance_cleaned.csv |
| risk_grade | TEXT | Risk grade assigned to fund | scheme_performance_cleaned.csv |

---

# fact_aum

| Column | Data Type | Business Definition | Source |
|----------|-----------|-------------------|--------|
| date | DATE | Reporting date | aum_by_fund_house_cleaned.csv |
| fund_house | TEXT | Asset management company | aum_by_fund_house_cleaned.csv |
| aum_lakh_crore | REAL | AUM in lakh crores | aum_by_fund_house_cleaned.csv |
| aum_crore | REAL | AUM in crores | aum_by_fund_house_cleaned.csv |
| num_schemes | INTEGER | Number of schemes managed | aum_by_fund_house_cleaned.csv |