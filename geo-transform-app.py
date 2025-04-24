
import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

st.title("2D Geometric Transformation Explorer")

# Input: ticker and date range
ticker = st.text_input("Enter Stock Ticker (e.g., AAPL):", "AAPL")
start = st.date_input("Start Date")
end = st.date_input("End Date")

# Load data if button clicked or already in session state
if st.button("Load & Transform Data") or "data" in st.session_state:
    if "data" not in st.session_state:
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            st.error("No data returned. Check the ticker and date range.")
            st.stop()
        st.session_state.data = data
    else:
        data = st.session_state.data

    st.write("Downloaded columns:", list(data.columns))  # Debug info

    # Pick appropriate price column
    price_col = None
    for col in ["Adj Close", "Close", "Open", "High", "Low"]:
        if col in data.columns:
            price_col = col
            break

    if not price_col:
        st.error("Could not find any price column in the data.")
        st.stop()

    prices = data[price_col].values

    # Generate x and y
    x = np.arange(len(prices))
    y = prices

    # Ensure x and y are 1D and same length
    x = np.ravel(x)
    y = np.ravel(y)
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]
    points = np.vstack((x, y))

    # Plot original
    st.subheader("Original Plot")
    fig1, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_title("Original Price Curve")
    st.pyplot(fig1)

    # Matrix input
    st.subheader("Enter 2D Transformation Matrix")
    a11 = st.number_input("a11", value=1.0)
    a12 = st.number_input("a12", value=0.0)
    a21 = st.number_input("a21", value=0.0)
    a22 = st.number_input("a22", value=1.0)

    transform = np.array([[a11, a12], [a21, a22]])

    # Apply transformation
    transformed_points = transform @ points

    # Plot transformed
    st.subheader("Transformed Plot")
    fig2, ax2 = plt.subplots()
    ax2.plot(transformed_points[0], transformed_points[1])
    ax2.set_title("Transformed Curve")
    st.pyplot(fig2)

# Optional: Reset button to clear session state
if st.button("Reset App"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.experimental_rerun()
