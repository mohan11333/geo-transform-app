import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Portfolio Optimization App")

st.sidebar.header("Portfolio Inputs")
tickers = st.sidebar.text_input("Enter tickers separated by commas (e.g. AAPL,MSFT,GOOG)", "AAPL,MSFT,GOOG")
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2020-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("2023-01-01"))

tickers = [ticker.strip().upper() for ticker in tickers.split(",")]

@st.cache_data
def get_data(tickers, start, end):
    data = yf.download(tickers, start=start, end=end)["Adj Close"]
    return data

data = get_data(tickers, start_date, end_date)
returns = data.pct_change().dropna()

st.subheader("Stock Prices")
st.line_chart(data)

st.subheader("Portfolio Simulation")

def simulate_portfolios(returns, num_portfolios=5000, risk_free_rate=0.01):
    mean_returns = returns.mean() * 252
    cov_matrix = returns.cov() * 252
    num_assets = len(returns.columns)
    
    results = np.zeros((3, num_portfolios))
    weights_record = []

    for i in range(num_portfolios):
        weights = np.random.random(num_assets)
        weights /= np.sum(weights)
        weights_record.append(weights)

        portfolio_return = np.dot(weights, mean_returns)
        portfolio_stddev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
        sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_stddev

        results[0, i] = portfolio_return
        results[1, i] = portfolio_stddev
        results[2, i] = sharpe_ratio

    return results, weights_record

results, weights_record = simulate_portfolios(returns)
max_sharpe_idx = np.argmax(results[2])
max_sharpe_allocation = weights_record[max_sharpe_idx]

fig, ax = plt.subplots()
scatter = ax.scatter(results[1,:], results[0,:], c=results[2,:], cmap='viridis')
ax.scatter(results[1, max_sharpe_idx], results[0, max_sharpe_idx], c='red', marker='*', s=100)
ax.set_xlabel('Volatility (Std. Deviation)')
ax.set_ylabel('Expected Return')
ax.set_title('Portfolio Optimization - Monte Carlo Simulation')
fig.colorbar(scatter, label='Sharpe Ratio')
st.pyplot(fig)

st.subheader("Optimized Portfolio Allocation")
for i, ticker in enumerate(tickers):
    st.write(f"{ticker}: {max_sharpe_allocation[i]*100:.2f}%")

st.write(f"Expected return: {results[0, max_sharpe_idx]*100:.2f}%")
st.write(f"Volatility: {results[1, max_sharpe_idx]*100:.2f}%")
st.write(f"Sharpe Ratio: {results[2, max_sharpe_idx]:.2f}")
