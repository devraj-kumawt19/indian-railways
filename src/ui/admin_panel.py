import streamlit as st
from src.auth.jwt_auth import create_access_token, verify_token
from src.db.mongo import get_db
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def admin_panel():
    st.header('Admin Panel')
    token = st.text_input('JWT Token', type='password')
    if token:
        try:
            payload = verify_token(token)
            st.success('Authenticated: ' + str(payload.get('sub')))
            db = get_db()
            if st.button('Show recent accuracy records'):
                recs = list(db.accuracy_metrics.find().sort('timestamp', -1).limit(20))
                st.write(recs)
        except Exception as e:
            st.error('Invalid token')

    st.markdown('Generate a short-lived token for administration:')
    subject = st.text_input('Subject (username/email)')
    ttl = st.number_input('TTL minutes', min_value=1, value=60)
    if st.button('Create token') and subject:
        tok = create_access_token(subject, expires_minutes=int(ttl))
        st.code(tok)
