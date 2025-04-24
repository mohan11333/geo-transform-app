

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

    st.write("Downloaded columns:", list(data.columns))  # Debug line

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

    # Create 2D points (x: normalized time, y: price)
    x = np.arange(len(prices))
    y = prices

    # Print debug information
    print(len(x), len(y))
    print(type(x), type(y))

    # Convert to numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Normalize x to be between 0 and 1
    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]

    # Normalize x to be between 0 and 1
    x = np.linspace(0, 1, min_len)  # x: normalized time
    y = y[:min_len]                  # y: prices

    points = np.vstack((x, y))

    st.subheader("Original Plot")
    fig1, ax1 = plt.subplots()
    ax1.plot(x, y)
    ax1.set_title("Original Price Curve")
    st.pyplot(fig1)

if transformation_type == "Scale":
    scale_factor = st.number_input("Scale Factor", value=1.0)
    transform = np.array([[scale_factor, 0], [0, scale_factor]])
elif transformation_type == "Rotate":
    angle = st.number_input("Rotation Angle (degrees)", value=0.0)
    radians = np.radians(angle)
    transform = np.array([[np.cos(radians), -np.sin(radians)], [np.sin(radians), np.cos(radians)]])
elif transformation_type == "Translate":
    tx = st.number_input("Translate X", value=0.0)
    ty = st.number_input("Translate Y", value=0.0)
    transform = np.array([[1, 0], [0, 1]])  # Translation is not a linear transformation, handle separately
    transformed_points[0] += tx
    transformed_points[1] += ty
else:
    transform = np.array([[1, 0], [0, 1]])  # Identity transformation
