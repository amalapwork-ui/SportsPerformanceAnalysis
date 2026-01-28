import streamlit as st
import requests

API_URL = "http://127.0.0.1:8001"

st.set_page_config(
    page_title="Sports Analytics Platform",
    layout="wide"
)

st.title("⚽ Sports Performance Analytics")
st.markdown("ML-powered football player analysis dashboard")

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
menu = st.sidebar.radio(
    "Select Module",
    ["Player Performance Prediction", "Injury Risk Assessment", "Video Player Tracking"]
)

# -----------------------------
# PLAYER PERFORMANCE
# -----------------------------
if menu == "Player Performance Prediction":
    st.header("📊 Player Performance Prediction")

    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", 16, 40, 24)
        potential = st.slider("Potential", 50, 95, 85)
        stamina = st.slider("Stamina", 30, 99, 80)

    with col2:
        strength = st.slider("Strength", 30, 99, 75)
        sprint_speed = st.slider("Sprint Speed", 30, 99, 90)
        work_rate_encoded = st.selectbox(
            "Work Rate (Encoded)",
            [0, 1, 2, 3, 4]
        )

    if st.button("Predict Performance"):
        payload = {
            "age": age,
            "potential": potential,
            "stamina": stamina,
            "strength": strength,
            "sprint_speed": sprint_speed,
            "work_rate_encoded": work_rate_encoded
        }

        response = requests.post(f"{API_URL}/predict", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success("Prediction Successful")
            st.metric("Predicted Overall", result["predicted_overall"])
            st.metric("Market Value (€)", f"{result['predicted_value_eur']:,}")
        else:
            st.error("API Error")

# -----------------------------
# INJURY RISK
# -----------------------------
elif menu == "Injury Risk Assessment":
    st.header("🩺 Injury Risk Assessment")

    age = st.slider("Age", 16, 40, 28)
    stamina = st.slider("Stamina", 30, 99, 70)
    work_rate = st.selectbox("Work Rate", [1, 2, 3, 4, 5])

    if st.button("Assess Injury Risk"):
        payload = {
            "age": age,
            "stamina": stamina,
            "work_rate": work_rate
        }

        response = requests.post(f"{API_URL}/injury-risk", json=payload)

        if response.status_code == 200:
            risk = response.json()["injury_risk"]
            if risk == "High":
                st.error("🚨 High Injury Risk")
            elif risk == "Medium":
                st.warning("⚠ Medium Injury Risk")
            else:
                st.success("✅ Low Injury Risk")

# -----------------------------
# VIDEO PLAYER TRACKING
# -----------------------------
# elif menu == "Video Player Tracking":
#     st.header("🎥 Player Detection & Tracking (YOLOv8)")

#     uploaded_file = st.file_uploader(
#         "Upload Football Match Video",
#         type=["mp4"]
#     )

#     if uploaded_file and st.button("Process Video"):
#         with st.spinner("Processing video..."):
#             files = {"file": uploaded_file.getvalue()}
#             response = requests.post(
#                 f"{API_URL}/process-video",
#                 files={"file": uploaded_file}
#             )

#         if response.status_code == 200:
#             st.success("Video processed successfully!")
#             st.json(response.json())
#         else:
#             st.error("Video processing failed")
elif menu == "Video Player Tracking":
    st.header("🎥 Player Detection & Tracking (YOLOv8)")

    uploaded_file = st.file_uploader(
        "Upload Football Match Video",
        type=["mp4"]
    )

    if uploaded_file and st.button("Process Video"):
        with st.spinner("Processing video..."):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    "video/mp4"
                )
            }

            response = requests.post(
                f"{API_URL}/process-video",
                files=files
            )

        if response.status_code == 200:
            st.success("Video processed successfully!")
            # st.json(response.json())
        else:
            st.error(f"API Error: {response.text}")
