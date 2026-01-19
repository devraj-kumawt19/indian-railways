import streamlit as st

st.title("🚂 Indian Train AI Detection System")

st.header("Live Camera Feed")
st.text("Camera feed will appear here (OpenCV not installed yet)")

st.header("Detection Results")
st.text("Detection results will appear here")

st.header("Train Status")
st.write("**Train 12301 (Rajdhani Express)**")
st.write("Platform: 1")
st.write("Scheduled: 08:00")
st.write("Status: On Time")

st.write("**Train 12302 (Shatabdi Express)**")
st.write("Platform: 2")
st.write("Scheduled: 10:30")
st.write("Status: Arriving")

st.success("Project is running! Install OpenCV and YOLO models for full functionality.")