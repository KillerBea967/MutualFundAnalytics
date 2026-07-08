import pandas as pd
import numpy as np

from scipy.stats import linregress

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

def compute_daily_returns(nav_df):

    nav = nav_df.copy()

    nav["date"] = pd.to_datetime(nav["date"])

    nav = nav.sort_values(["amfi_code","date"])

    nav["daily_return"] = (
        nav.groupby("amfi_code")["nav"]
        .pct_change()
    )

    return nav

def plot_return_distribution(nav_df):

    plt.figure(figsize=(12,6))

    sns.histplot(
        nav_df["daily_return"].dropna(),
        bins=60,
        kde=True
    )

    plt.title("Daily Return Distribution")

    plt.show()

import pandas as pd
import numpy as np

def compute_cagr(nav_df):

    nav = nav_df.copy()

    nav["date"] = pd.to_datetime(nav["date"])

    results = []

    for fund, group in nav.groupby("amfi_code"):

        group = group.sort_values("date")

        start_nav = group.iloc[0]["nav"]
        end_nav = group.iloc[-1]["nav"]

        # Number of trading periods
        trading_days = len(group) - 1

        if trading_days <= 0:
            continue

        cagr = (
            (end_nav / start_nav)
            ** (252 / trading_days)
        ) - 1

        results.append({

            "amfi_code": fund,

            "Start_NAV": start_nav,

            "End_NAV": end_nav,

            "Trading_Days": trading_days,

            "CAGR": cagr

        })

    return pd.DataFrame(results)

def sharpe_ratio(nav_df,risk_free=0.065):

    returns = compute_daily_returns(nav_df)

    sharpe=[]

    for fund,group in returns.groupby("amfi_code"):

        r = group["daily_return"].dropna()

        excess = r-(risk_free/252)

        sr = np.sqrt(252)*excess.mean()/r.std()

        sharpe.append({

            "amfi_code":fund,

            "Sharpe":sr

        })

    return (
        pd.DataFrame(sharpe)
        .sort_values("Sharpe",ascending=False)
    )

def sortino_ratio(nav_df,risk_free=0.065):

    returns = compute_daily_returns(nav_df)

    output=[]

    for fund,group in returns.groupby("amfi_code"):

        r=group["daily_return"].dropna()

        downside=r[r<0]

        downside_std=downside.std()

        sr=np.sqrt(252)*(r.mean()-risk_free/252)/downside_std

        output.append({

            "amfi_code":fund,

            "Sortino":sr

        })

    return pd.DataFrame(output)

from scipy.stats import linregress

def alpha_beta(nav_df, benchmark_df):

    nav_returns = compute_daily_returns(nav_df)

    results = []

    for fund, group in nav_returns.groupby("amfi_code"):

        merged = group.merge(
            benchmark_df[["date", "benchmark_return"]],
            on="date",
            how="inner"
        )

        merged = merged.dropna(
            subset=["daily_return", "benchmark_return"]
        )

        if len(merged) < 30:
            continue

        beta, alpha, r_value, p_value, std_err = linregress(
            merged["benchmark_return"],
            merged["daily_return"]
        )

        results.append({
            "amfi_code": fund,
            "Alpha": alpha * 252,
            "Beta": beta,
            "R_squared": r_value**2
        })

    return pd.DataFrame(results)

def maximum_drawdown(nav_df):

    output=[]

    for fund,group in nav_df.groupby("amfi_code"):

        group=group.sort_values("date")

        running_max=group["nav"].cummax()

        drawdown=group["nav"]/running_max-1

        output.append({

            "amfi_code":fund,

            "Max_Drawdown":drawdown.min()

        })

    return pd.DataFrame(output)

def fund_scorecard(

    performance,

    sharpe,

    alpha,

    drawdown

):

    score=performance.copy()

    score=score.merge(

        sharpe,

        on="amfi_code"

    )

    score=score.merge(

        alpha,

        on="amfi_code"

    )

    score=score.merge(

        drawdown,

        on="amfi_code"

    )

    score["ReturnRank"]=score["return_3yr_pct"].rank()

    score["SharpeRank"]=score["Sharpe"].rank()

    score["AlphaRank"]=score["Alpha"].rank()

    score["ExpenseRank"]=(-score["expense_ratio_pct"]).rank()

    score["DrawRank"]=(-score["Max_Drawdown"]).rank()

    score["Score"]=(
        0.30*score["ReturnRank"]+
        0.25*score["SharpeRank"]+
        0.20*score["AlphaRank"]+
        0.15*score["ExpenseRank"]+
        0.10*score["DrawRank"]
    )

    score["Score"]=100*score["Score"]/score["Score"].max()

    return score.sort_values(
        "Score",
        ascending=False
    )