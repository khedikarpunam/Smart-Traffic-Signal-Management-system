import streamlit as st
import numpy as np
from PIL import Image
import time
from ultralytics import YOLO

st.set_page_config(page_title="Smart Traffic AI", layout="wide")

st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🚦 Smart Traffic Signal System")
st.write("AI-powered real-time traffic analysis and signal control.")
st.markdown("---")

model = YOLO("yolov8n.pt")

VEHICLE_CLASSES = ['car', 'truck', 'bus', 'motorcycle', 'bicycle']

uploaded_file = st.file_uploader("Upload Traffic Image:", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Traffic Scenario', use_container_width=True)

    with st.spinner('AI analyzing traffic...'):
        results = model(image)
        counts = results[0].boxes.cls.tolist()
        names = results[0].names
        vehicle_count = sum(1 for c in counts if names[int(c)] in VEHICLE_CLASSES)

    if vehicle_count > 25:
        traffic_level = "HIGH"
        signal_time = "90 seconds"
        decision = "Heavy traffic detected. **Green signal duration increased.**"
        status_color = "red"
    elif vehicle_count > 10:
        traffic_level = "MEDIUM"
        signal_time = "60 seconds"
        decision = "Normal traffic. **Standard signal timing applied.**"
        status_color = "orange"
    else:
        traffic_level = "LOW"
        signal_time = "30 seconds"
        decision = "Low traffic. **Reduced green signal to save time.**"
        status_color = "green"

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="metric-card"><h3>Veh🚗icle</h3><h2 style="color:#1f77b4;">{vehicle_count}</h2></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>Den📊sity</h3><h2 style="color:{status_color};">{traffic_level}</h2></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>Ti🕒mer</h3><h2 style="color:green;">{signal_time}</h2></div>', unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("AI Decision:")
    st.info(decision)

else:
    st.warning("Please upload a traffic image to start the analysis.")

st.markdown("---")
st.caption("Developed for Smart City Project - 2026")