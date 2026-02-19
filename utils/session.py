import streamlit as st


def init_session_state():
    defaults = {
        "df": None,
        "df_raw": None,
        "chat_history": [],
        "file_name": ""
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value