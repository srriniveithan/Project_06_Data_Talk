import streamlit as st
import pandas as pd
from llm_engine import chat_with_data
from viz_engine import render_chart


def render(groq_api_key, groq_model):
    st.title("💬 Chat with Your Data")

    if st.session_state.df is None:
        st.info("Please upload a dataset first.")
        return

    if not groq_api_key:
        st.warning("Please enter your Groq API key in the sidebar to use the chat feature.")
        return

    df = st.session_state.df

    st.write(f"**File:** {st.session_state.file_name} | **Shape:** {df.shape[0]} rows × {df.shape[1]} columns")
    st.divider()

    # ── Quick question buttons at the top ──────────────────────────────
    st.write("**Quick questions:**")
    btn_cols = st.columns(4)
    quick_questions = [
        "Summarize this dataset",
        "Which columns have missing values?",
        "Show top 10 rows by first numeric column",
        "Give me key insights from the data"
    ]

    clicked_quick = None
    for i, question in enumerate(quick_questions):
        with btn_cols[i]:
            if st.button(question, key=f"qbtn_{i}", use_container_width=True):
                clicked_quick = question

    st.divider()

    # ── Chat input form ────────────────────────────────────────────────
    with st.form("chat_form", clear_on_submit=True):
        col_a, col_b = st.columns([5, 1])
        with col_a:
            user_question = st.text_input(
                "Type your question",
                placeholder="e.g. How many missing values are there?",
                label_visibility="collapsed"
            )
        with col_b:
            send_btn = st.form_submit_button("Send 🚀", use_container_width=True)

    # ── Determine final question ───────────────────────────────────────
    final_question = None
    if send_btn and user_question.strip():
        final_question = user_question.strip()
    elif clicked_quick:
        final_question = clicked_quick

    # ── Process the question ───────────────────────────────────────────
    if final_question:
        # Add user message to history immediately
        st.session_state.chat_history.append({"role": "user", "content": final_question})

        with st.spinner("Thinking..."):
            reply, chart_info, code_result, error = chat_with_data(
                df,
                final_question,
                st.session_state.chat_history[:-1],  # exclude the just-added message
                groq_api_key,
                groq_model
            )

        if error and not reply:
            st.session_state.chat_history.pop()  # remove the unanswered question
            st.error(f"❌ {error}")
        elif reply:
            st.session_state.chat_history.append({"role": "assistant", "content": reply})

    # ── Display all chat messages ──────────────────────────────────────
    if len(st.session_state.chat_history) == 0:
        st.markdown("""
        <div style='text-align: center; color: gray; padding: 30px;'>
            <h3>Ask anything about your data!</h3>
            <p>Use the quick questions above or type your own below.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.chat_history:
            if message["role"] == "user":
                st.markdown(
                    f'<div class="chat-user">🧑 {message["content"]}</div>',
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f'<div class="chat-bot">🤖 {message["content"]}</div>',
                    unsafe_allow_html=True
                )

        # Show chart for the last reply if suggested
        if final_question and chart_info:
            x = chart_info.get("x_col")
            y = chart_info.get("y_col")
            ctype = chart_info.get("chart_type", "bar")

            if x and x in df.columns:
                y = y if y and y in df.columns else None
                try:
                    img = render_chart(df, ctype, x, y, title=final_question)
                    st.image(img, use_container_width=True)
                    st.download_button(
                        "Download Chart",
                        data=img,
                        file_name="chart.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.warning(f"Could not render chart: {e}")

        # Show computed result if any
        if final_question and code_result is not None:
            st.write("**Computed Result:**")
            if isinstance(code_result, pd.DataFrame):
                st.dataframe(code_result, use_container_width=True)
            else:
                st.write(code_result)

    st.divider()

    # Clear chat button
    if len(st.session_state.chat_history) > 0:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = []
            st.rerun()