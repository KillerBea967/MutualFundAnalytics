CREATE TABLE dim_fund (
    amfi_code INTEGER PRIMARY KEY,
    scheme_name TEXT NOT NULL,
    fund_house TEXT NOT NULL,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    fund_manager TEXT,
    risk_category TEXT
);

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    year INTEGER NOT NULL,
    quarter INTEGER NOT NULL,
    month INTEGER NOT NULL,
    month_name TEXT,
    day INTEGER NOT NULL,
    weekday_name TEXT,
    is_weekend INTEGER
);

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    nav REAL NOT NULL,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    investor_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    amfi_code INTEGER NOT NULL,

    transaction_type TEXT,
    amount_inr REAL NOT NULL,

    state TEXT,
    city TEXT,
    city_tier TEXT,

    age_group TEXT,
    gender TEXT,
    annual_income_lakh REAL,

    payment_mode TEXT,
    kyc_status TEXT,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);


CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER NOT NULL,

    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,

    benchmark_3yr_pct REAL,

    alpha REAL,
    beta REAL,

    sharpe_ratio REAL,
    sortino_ratio REAL,

    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,

    morningstar_rating INTEGER,

    FOREIGN KEY (amfi_code)
        REFERENCES dim_fund(amfi_code)
);

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    date_id INTEGER NOT NULL,

    fund_house TEXT NOT NULL,

    aum_lakh_crore REAL,
    aum_crore REAL,

    num_schemes INTEGER,

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);