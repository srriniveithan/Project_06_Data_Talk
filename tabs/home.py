import streamlit as st


def render():
    st.title("👋 Welcome to DataTalk")
    st.subheader("Conversational Data Analysis & Auto-Visualization System")
    st.divider()

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        **DataTalk** helps you understand your data without writing any code.

        Here's what you can do:
        - 📂 Upload any CSV or Excel file
        - 📊 Get automatic charts, statistics, and insights
        - 💬 Ask questions about your data in plain English
        - 📈 Build custom visualizations with a few clicks

        **Steps to get started:**
        1. Go to the **Upload Dataset** tab
        2. Upload your CSV or Excel file
        3. Explore the **EDA Dashboard**
        4. Chat with your data in the **Chat** tab
        """)

    with col2:
        st.info("""
        **Example questions you can ask:**

        - "What is the average sales?"
        - "Which region has the highest revenue?"
        - "Show me the monthly trend"
        - "Are there missing values?"
        - "Plot price distribution"
        """)

    st.divider()
    st.markdown("### Why DataTalk?")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("LLM", "Groq Llama 3")
    with c2:
        st.metric("Charts", "6 Types")
    with c3:
        st.metric("File Support", "CSV & Excel")
    with c4:
        st.metric("Cost", "Free to Use")