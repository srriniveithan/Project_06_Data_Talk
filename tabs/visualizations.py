import streamlit as st
import numpy as np
from viz_engine import render_chart, infer_best_chart


def render():
    st.title("📈 Auto Visualizations")

    if st.session_state.df is None:
        st.info("Please upload a dataset first.")
        return

    df = st.session_state.df
    all_columns = df.columns.tolist()
    numeric_columns = df.select_dtypes(include=np.number).columns.tolist()
    categorical_columns = df.select_dtypes(include="object").columns.tolist()

    st.subheader("Chart Builder")

    col1, col2, col3 = st.columns(3)

    with col1:
        chart_type = st.selectbox(
            "Chart Type",
            options=["auto", "bar", "line", "scatter", "histogram", "boxplot", "pie"],
            help="Select 'auto' to let the system choose"
        )

    with col2:
        x_column = st.selectbox("X-Axis", options=all_columns)

    with col3:
        y_options = ["None"] + numeric_columns
        y_raw = st.selectbox("Y-Axis (optional)", options=y_options)
        y_column = None if y_raw == "None" else y_raw

    col4, col5 = st.columns(2)
    with col4:
        aggregation = st.selectbox(
            "Aggregation (for bar/line charts)",
            options=["mean", "sum", "count", "max", "min", "median"]
        )
    with col5:
        custom_title = st.text_input("Chart Title (optional)")

    st.divider()

    if st.button("Generate Chart", type="primary", use_container_width=True):
        try:
            selected_type = chart_type

            if chart_type == "auto":
                selected_type = infer_best_chart(df, x_column, y_column)
                st.info(f"Auto-selected chart type: {selected_type}")

            with st.spinner("Generating chart..."):
                chart_img = render_chart(
                    df,
                    selected_type,
                    x_column,
                    y_column,
                    agg_func=aggregation,
                    title=custom_title
                )

            st.image(chart_img, use_container_width=True)

            st.download_button(
                "Download Chart as PNG",
                data=chart_img,
                file_name=f"{selected_type}_{x_column}.png",
                mime="image/png"
            )

        except Exception as e:
            st.error(f"Could not generate chart: {e}")

    st.divider()
    st.subheader("Quick Charts")
    st.write("Click any column below to instantly see its chart:")

    if numeric_columns:
        st.write("Numeric columns:")
        cols = st.columns(min(4, len(numeric_columns)))
        for i, col_name in enumerate(numeric_columns[:4]):
            with cols[i]:
                if st.button(col_name, key=f"num_btn_{i}", use_container_width=True):
                    img = render_chart(df, "histogram", col_name, title=f"Distribution of {col_name}")
                    st.image(img, use_container_width=True)

    if categorical_columns:
        st.write("Categorical columns:")
        cols2 = st.columns(min(4, len(categorical_columns)))
        for i, col_name in enumerate(categorical_columns[:4]):
            with cols2[i]:
                if st.button(col_name, key=f"cat_btn_{i}", use_container_width=True):
                    img = render_chart(df, "bar", col_name, title=f"Count of {col_name}")
                    st.image(img, use_container_width=True)