import pandas as pd
import numpy as np
import plotly.express as px

def compute_daily_returns(nav_df):
    df = nav_df.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values(["amfi_code", "date"])
    df["daily_return"] = (
        df.groupby("amfi_code")["nav"]
        .pct_change()
    )

    return df

def historical_var_cvar(nav_df, confidence=0.95):
    returns = compute_daily_returns(nav_df)
    output = []
    percentile = (1 - confidence) * 100
    for fund, group in returns.groupby("amfi_code"):
        r = group["daily_return"].dropna()
        if len(r) == 0:
            continue
        var = np.percentile(r, percentile)
        cvar = r[r <= var].mean()
        output.append({
            "amfi_code": fund,
            "VaR_95": var,
            "CVaR_95": cvar
        })

    output = pd.DataFrame(output)
    output = output.sort_values(
        "VaR_95"
    )

    return output

def rolling_sharpe(nav_df, window=90):
    returns = compute_daily_returns(nav_df)
    output = []
    for fund, group in returns.groupby("amfi_code"):
        group = group.sort_values("date")
        rolling = (
            group["daily_return"]
            .rolling(window)
            .mean()
            /
            group["daily_return"]
            .rolling(window)
            .std()
        ) * np.sqrt(252)

        temp = pd.DataFrame({
            "date": group["date"],
            "amfi_code": fund,
            "Rolling_Sharpe": rolling
        })

        output.append(temp)
    output = pd.concat(
        output,
        ignore_index=True
    )

    return output


def plot_rolling_sharpe(
    rolling_df,
    funds
):
    df = rolling_df[
        rolling_df["amfi_code"].isin(funds)
    ]
    fig = px.line(
        df,
        x="date",
        y="Rolling_Sharpe",
        color="amfi_code",
        title="Rolling 90-Day Sharpe Ratio"
    )

    fig.show()

def investor_cohort_analysis(
    investor_df
):
    df = investor_df.copy()
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )
    first_year = (
        df.groupby("investor_id")[
            "transaction_date"
        ]
        .min()
        .dt.year
    )

    df["cohort"] = (
        df["investor_id"]
        .map(first_year)
    )

    top_fund = (
        df.groupby(
            ["cohort", "amfi_code"]
        )
        .size()
        .reset_index(name="count")
        .sort_values(
            ["cohort", "count"],
            ascending=False
        )
        .drop_duplicates(
            "cohort"
        )
    )

    summary = (
        df.groupby("cohort")
        .agg(
            Average_Investment=("amount_inr", "mean"),
            Total_Investment=("amount_inr", "sum"),
            Investors=("investor_id", "nunique")
        )
        .reset_index()
    )

    summary = summary.merge(
        top_fund[
            ["cohort", "amfi_code"]
        ],
        on="cohort"
    )

    summary.rename(
        columns={
            "amfi_code":
            "Top_Fund"
        },
        inplace=True
    )

    return summary

def sip_continuity_analysis(
    investor_df
):
    df = investor_df.copy()
    df = df[
        df["transaction_type"] == "SIP"
    ]
    df["transaction_date"] = pd.to_datetime(
        df["transaction_date"]
    )

    output = []
    for investor, group in df.groupby(
        "investor_id"
    ):
        if len(group) < 6:
            continue
        group = group.sort_values(
            "transaction_date"
        )
        gap = (
            group["transaction_date"]
            .diff()
            .dt.days
        )

        avg_gap = gap.mean()
        output.append({
            "investor_id": investor,
            "No_of_SIPs": len(group),
            "Average_Gap": avg_gap,
            "Status":
                "At-Risk"
                if avg_gap > 35
                else "Regular"
        })

    return pd.DataFrame(output)

def recommend_funds(
    performance_df,
    sharpe_df,
    risk_level
):

    df = performance_df.merge(
        sharpe_df,
        on="amfi_code"
    )

    df = df[
        df["risk_grade"]
        .str.lower()
        ==
        risk_level.lower()
    ]

    df = df.sort_values(
        "Sharpe",
        ascending=False
    )
    cols = [
        "scheme_name",
        "fund_house",
        "risk_grade",
        "Sharpe",
        "return_3yr_pct",
        "expense_ratio_pct"
    ]
    return df[cols].head(3)

def sector_hhi(
    portfolio_df
):
    output = []
    for fund, group in portfolio_df.groupby(
        "amfi_code"
    ):
        weights = (
            group["weight_pct"]
            / 100
        )
        hhi = np.sum(
            weights ** 2
        )
        output.append({
            "amfi_code": fund,
            "HHI": hhi
        })
    output = pd.DataFrame(output)
    output = output.sort_values(
        "HHI",
        ascending=False
    )
    return output