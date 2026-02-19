import streamlit as st


def render():
    st.title("👤 About This Project")
    st.divider()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### DataTalk — Conversational Data Analysis & Auto-Visualization System

        This project was built as a **capstone project** for the GUVI | HCL Data Science program.

        The goal of this project is to make data analysis accessible to everyone —
        even people who don't know Python or SQL. Users can simply upload their data
        and ask questions in plain English.

        ---

        ### Tech Stack

        | Component | Tool Used |
        |-----------|-----------|
        | Web App | Streamlit |
        | AI / LLM | Groq (Llama 3 70B) |
        | Data Handling | Pandas, NumPy |
        | Charts | Matplotlib, Seaborn |
        | Language | Python |

        ---

        ### What This App Can Do

        - Upload and preview any CSV or Excel dataset
        - Automatically clean and prepare the data
        - Show statistics, correlations, distributions, and outliers
        - Answer natural language questions about the data
        - Generate charts automatically based on the question
        - Let users build custom charts manually

        ---

        ### Domain
        Data Science · Analytics · Business Intelligence · Automation
        """)

    with col2:
        st.info("""
        **Supported File Formats:**
        CSV, XLSX, XLS

        **Available LLM Models:**
        - llama3-70b-8192
        - llama3-8b-8192
        - mixtral-8x7b-32768
        - gemma2-9b-it

        **Chart Types:**
        Bar, Line, Scatter,
        Histogram, Boxplot, Pie

        **Get Free Groq API Key:**
        Visit console.groq.com
        """)

    st.divider()
    st.caption("Built using Python · Streamlit · Groq · Pandas · Matplotlib · Seaborn")