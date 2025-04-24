import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

st.title("2D Geometric Transformation Explorer")

# Get ticker and dates
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
start = st.date_input("Start Date")
end = st.date_input("End Date")

if st.button("Load & Transform Data"):
    data = yf.download(ticker, start=start, end=end)

    if data.empty:
        st.error("No data returned. Check the ticker and date range.")
        st.stop()

    st.write("Downloaded columns:", list(data.columns))  # <--- Debug line

    # Fix: Use the first available price column
    price_col = None
    for col in ["Adj Close", "Close", "Open", "High", "Low"]:
        if col in data.columns:
            price_col = col
            break

    if not price_col:
        st.error("Could not find any price column (Adj Close, Close, etc.) in the data.")
        st.stop()

    prices = data[price_col].values

    # Now continue with transformation…
    # Create 2D points (x: time step, y: price)
    x = np.arange(len(prices))
    y = prices
    points = np.vstack((x, y))

    st.subheader("Original Plot")
    fig1, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_title("Original Price Curve")
    st.pyplot(fig1)

    # Get transformation matrix input
    st.subheader("Enter 2D Transformation Matrix")
    a11 = st.number_input("a11", value=1.0)
    a12 = st.number_input("a12", value=0.0)
    a21 = st.number_input("a21", value=0.0)
    a22 = st.number_input("a22", value=1.0)

    transform = np.array([[a11, a12], [a21, a22]])

    # Apply transformation
    transformed_points = transform @ points

    st.subheader("Transformed Plot")
    fig2, ax2 = plt.subplots()
    ax2.plot(transformed_points[0], transformed_points[1])
    ax2.set_title("Transformed Curve")
    st.pyplot(fig2)
