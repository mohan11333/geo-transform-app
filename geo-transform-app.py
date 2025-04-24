
import streamlit as st
import pandas as pd
import numpy as np
import pyproj
import json

st.title("Geo Coordinate Transformer")

uploaded_file = st.file_uploader("Upload a JSON file", type="json")

if uploaded_file is not None:
    data = json.load(uploaded_file)

    # Display structure
    st.subheader("JSON Structure")
    st.json(data)

    # Extract values assuming format is like: [[lat1, lon1], [lat2, lon2], ...]
    x, y = [], []
    for item in data:
        if isinstance(item, list) and len(item) >= 2:
            x.append(item[0])
            y.append(item[1])

    # Ensure x and y are numpy arrays and have matching lengths
    x = np.array(x)
    y = np.array(y)

    if len(x) == 0 or len(y) == 0:
        st.error("x or y array is empty — cannot stack empty arrays.")
        st.stop()

    min_len = min(len(x), len(y))
    x = x[:min_len]
    y = y[:min_len]

    # Stack into a 2D array for projection
    points = np.vstack((x, y))

    # Transformer (example from WGS84 to Web Mercator)
    transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
    transformed_x, transformed_y = transformer.transform(points[0], points[1])

    # Create DataFrame and show
    df = pd.DataFrame({
        'Original_Lon': points[0],
        'Original_Lat': points[1],
        'Transformed_X': transformed_x,
        'Transformed_Y': transformed_y
    })

    st.subheader("Transformed Coordinates")
    st.dataframe(df)

    # Option to download result
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        "Download Transformed Data as CSV",
        data=csv,
        file_name="transformed_coordinates.csv",
        mime="text/csv"
    )
