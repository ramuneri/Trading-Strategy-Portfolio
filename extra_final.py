import math
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
import matplotlib.pyplot as plt

# ============================================================
# PARAMETERS
# ============================================================

tickers = ["AAPL", "META", "TSLA"]
start = "2018-01-01"
end = "2024-01-01"

# ============================================================
# SLIDING AVERAGE STRATEGY (MA20 / MA50)
# ============================================================

def ma_strategy(price_series):
    """Simple Moving Average strategy: MA20 > MA50 = BUY"""

    # FIX: ensure we're working with a Series
    if isinstance(price_series, pd.DataFrame):
        if "Close" in price_series.columns:
            price_series = price_series["Close"]
        else:
            price_series = price_series.iloc[:, 0]

    df = price_series.to_frame(name="Close").copy()

    df["MA20"] = df["Close"].rolling(20).mean()
    df["MA50"] = df["Close"].rolling(50).mean()

    df["Signal"] = 0
    df.loc[df["MA20"] > df["MA50"], "Signal"] = 1

    df["Return"] = df["Close"].pct_change()
    df["Strategy_return"] = (df["Return"] * df["Signal"].shift(1)).fillna(0)

    df["Equity"] = (1 + df["Strategy_return"]).cumprod()
    return df



# ============================================================
# APPLY STRATEGY TO ALL TICKERS
# ============================================================

results = {}
all_returns = []

for t in tickers:
    data = yf.download(t, start=start, end=end, auto_adjust=True)

    # ALWAYS get a Series:
    price = data["Close"].astype(float)

    df = ma_strategy(price)
    results[t] = df
    all_returns.append(df["Strategy_return"].rename(t))


# DataFrame of strategy returns for all tickers
returns_df = pd.concat(all_returns, axis=1).dropna()

# ============================================================
# INDIVIDUAL EQUITY GRAPHS (STRATEGY PROFIT)
# ============================================================

plt.figure(figsize=(18, 4))
cols = 4
rows = 1 

for i, t in enumerate(tickers):
    plt.subplot(rows, cols, i + 1)
    plt.plot(results[t]["Equity"])
    plt.title(f"{t} Strategy Equity (MA 20/50)")
    plt.grid(True)

plt.tight_layout()



# ============================================================
# PORTFOLIO (EQUAL WEIGHT)
# ============================================================

portfolio_returns = returns_df.mean(axis=1)
portfolio_equity = (1 + portfolio_returns).cumprod()

plt.subplot(rows, cols, len(tickers)+1)
plt.plot(portfolio_equity)
plt.title("Equal-Weight Portfolio Equity (MA 20/50)")
plt.grid(True)
plt.show()


# ============================================================
# CORRELATION MATRIX
# ============================================================

corr = returns_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1)
plt.title("SMA Strategy Return Correlation Matrix")
plt.show()
