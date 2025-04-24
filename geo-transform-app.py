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

    # Ensure x and y are numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Debug prints (optional, useful during testing)
    print("Length of x:", len(x))
    print("Length of y:", len(y))

    # Make sure x and y have the same length
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

    # Transformation options
    st.subheader("Select Transformation Type")
    transformation_type = st.selectbox("Choose a transformation", ["None", "Scale", "Rotate", "Translate"])

    # Initialize transformation matrix
    transform = np.eye(2)  # Identity matrix

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
        transformed_points = points.copy()  # Copy original points for translation
        transformed_points[0] += tx
        transformed_points[1] += ty
        st.subheader("Transformed Plot (Translation)")
        fig3, ax3 = plt.subplots()
        ax3.plot(transformed_points[0], transformed_points[1])
        ax3.set_title("Translated Curve")
        st.pyplot(fig3)
        st.stop()  # Stop here to avoid applying the transformation matrix

    # Apply transformation matrix for Scale and Rotate
    transformed_points = transform @ points

    st.subheader("Transformed Plot")
    fig2, ax2 = plt.subplots()
    ax2.plot(transformed_points[0], transformed_points[1])
    ax2.set_title("Transformed Curve")
    st.pyplot(fig2)
