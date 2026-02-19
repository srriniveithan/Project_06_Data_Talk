import streamlit as st
from utils.session import init_session_state
from tabs import home, upload, eda_tab, chat, visualizations, about
from data_prep import prepare_dataset

# -------------------------------------------------------
# Page configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="DataTalk",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------------
# Custom CSS styling
# -------------------------------------------------------
st.markdown("""
<style>
    .chat-user {
        background-color: #DCF8C6;
        border-radius: 10px;
        padding: 10px 15px;
        margin: 6px 0;
        margin-left: 25%;
    }
    .chat-bot {
        background-color: #F1F0F0;
        border-radius: 10px;
        padding: 10px 15px;
        margin: 6px 0;
        margin-right: 25%;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# Initialize session state
# -------------------------------------------------------
init_session_state()

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
with st.sidebar:
    st.title("💬 DataTalk")
    st.write("Conversational Data Analysis & Visualization")
    st.divider()

    st.subheader("Settings")
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        placeholder="Enter your Groq API key here",
        help="You can get a free key from console.groq.com"
    )

    groq_model = st.selectbox(
        "Choose LLM Model",
        options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "gemma2-9b-it", "mixtral-8x7b-32768"]
    )

    st.divider()

    # Data cleaning controls (only visible after upload)
    if st.session_state.df is not None:
        st.subheader("Data Cleaning")

        missing_strategy = st.selectbox(
            "Handle Missing Values",
            options=["none", "drop_rows", "drop_high_missing_cols", "fill_mean", "fill_median", "fill_mode"]
        )

        if st.button("Apply Cleaning"):
            st.session_state.df = prepare_dataset(
                st.session_state.df_raw,
                missing_strategy=missing_strategy
            )
            st.success("Cleaning applied!")

        st.divider()

        if st.button("Clear Dataset"):
            st.session_state.df = None
            st.session_state.df_raw = None
            st.session_state.chat_history = []
            st.rerun()

    st.divider()
    st.caption("Made with Streamlit, Groq, Pandas, Matplotlib")

# -------------------------------------------------------
# Main Tabs
# -------------------------------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Home",
    "📂 Upload Dataset",
    "📊 EDA Dashboard",
    "💬 Chat with Data",
    "📈 Visualizations",
    "👤 About"
])

with tab1:
    home.render()

with tab2:
    upload.render()

with tab3:
    eda_tab.render()

with tab4:
    chat.render(groq_api_key, groq_model)

with tab5:
    visualizations.render()

with tab6:
    about.render()