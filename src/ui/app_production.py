import os
import streamlit as st
from src.utils.logging_config import get_logger
from src.utils.haversine import distance_km
from src.services.live_rail_api import fetch_train_status
from src.services.accuracy import compute_accuracy_metrics
from src.utils.jwt_auth import create_token, decode_token

logger = get_logger("app_production")


def login_section():
    st.sidebar.header("Admin Login")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    if st.sidebar.button("Login"):
        # very small demo: compare to env vars for admin
        admin_user = os.getenv("ADMIN_USER", "admin")
        admin_pass = os.getenv("ADMIN_PASS", "password")
        if username == admin_user and password == admin_pass:
            token = create_token(username, roles=["admin"])
            st.session_state["jwt"] = token
            st.sidebar.success("Logged in as %s" % username)
        else:
            st.sidebar.error("Invalid credentials")


def show_train_layout(num_coaches: int = 10):
    st.header("Graphical Train Layout")
    cols = st.columns(min(num_coaches, 12))
    for i in range(num_coaches):
        c = cols[i % len(cols)]
        with c:
            st.button(f"Coach {i+1}")


def engine_distance_ui():
    st.subheader("Engine Distance Calculator")
    lat1 = st.number_input("Lat 1", value=28.6139)
    lon1 = st.number_input("Lon 1", value=77.2090)
    lat2 = st.number_input("Lat 2", value=19.0760)
    lon2 = st.number_input("Lon 2", value=72.8777)
    if st.button("Calculate Distance"):
        km = distance_km(lat1, lon1, lat2, lon2)
        st.success(f"Distance: {km:.2f} km")


def live_status_ui():
    st.subheader("Live Train Status")
    train_no = st.text_input("Train Number / ID")
    if st.button("Fetch Live Status") and train_no:
        try:
            data = fetch_train_status(train_no)
            st.json(data)
        except Exception as e:
            st.error(f"Failed to fetch live status: {e}")


def accuracy_demo_ui():
    st.subheader("Dynamic Accuracy Calculation")
    st.write("Provide true labels and predicted labels as comma-separated integers (0/1).")
    t = st.text_input("True labels", value="1,0,1,1,0")
    p = st.text_input("Predicted labels", value="1,0,0,1,0")
    if st.button("Compute Metrics"):
        y_true = [int(x.strip()) for x in t.split(",") if x.strip()]
        y_pred = [int(x.strip()) for x in p.split(",") if x.strip()]
        metrics = compute_accuracy_metrics(y_true, y_pred)
        st.json(metrics)


def main():
    st.title("Railway Coach Analytics — Production Preview")
    login_section()

    st.sidebar.markdown("---")
    page = st.sidebar.selectbox("Page", ["Dashboard", "Distance", "Live Status", "Accuracy", "Admin"])

    if page == "Dashboard":
        show_train_layout(num_coaches=12)
    elif page == "Distance":
        engine_distance_ui()
    elif page == "Live Status":
        live_status_ui()
    elif page == "Accuracy":
        accuracy_demo_ui()
    elif page == "Admin":
        token = st.session_state.get("jwt")
        if not token:
            st.error("Admin access requires login.")
        else:
            try:
                info = decode_token(token)
                st.write("Admin token info:")
                st.json(info)
                st.success("Admin panel — actions TBD (DB, logs, configs)")
            except Exception:
                st.error("Invalid token")


if __name__ == "__main__":
    main()
