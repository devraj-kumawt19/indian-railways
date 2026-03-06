import streamlit as st
import requests
from src.ui.train_layout import render_train_layout
from src.ui.admin_panel import admin_panel
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def main():
    st.set_page_config(page_title='Railway Coach Analytics', layout='wide')
    st.title('Railway Coach Analytics Platform')

    menu = st.sidebar.selectbox('Menu', ['Dashboard', 'Admin'])

    if menu == 'Admin':
        admin_panel()
        return

    st.sidebar.header('Distance Calculator')
    train_no = st.sidebar.text_input('Train number')
    if st.sidebar.button('Fetch Live') and train_no:
        try:
            resp = requests.get(f'http://localhost:8000/live/{train_no}', timeout=5).json()
            st.sidebar.write(resp)
        except Exception as e:
            st.sidebar.error('Failed to fetch live info')

    st.header('Train Layout')
    # example coaches
    coaches = [
        {'name': 'Engine', 'length_m': 15},
        {'name': 'S1', 'length_m': 24},
        {'name': 'S2', 'length_m': 24},
        {'name': 'S3', 'length_m': 24},
    ]
    render_train_layout(coaches, engine_position=0)


if __name__ == '__main__':
    main()
