import streamlit as st
import pandas as pd
from data_prep import load_dataset, prepare_dataset, get_dataset_summary


def render():
    st.title("📂 Upload Your Dataset")
    st.write("Upload a CSV or Excel file to get started.")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:
        try:
            with st.spinner("Reading file..."):
                df_raw = load_dataset(uploaded_file)
                df = prepare_dataset(df_raw, missing_strategy="none")

            # Save to session state so all tabs can access it
            st.session_state.df_raw = df_raw
            st.session_state.df = df
            st.session_state.file_name = uploaded_file.name
            st.session_state.chat_history = []

            st.success(f"File '{uploaded_file.name}' uploaded successfully!")

        except Exception as e:
            st.error(f"Something went wrong while reading the file: {e}")

    # Show dataset info if a file has been uploaded
    if st.session_state.df is not None:
        df = st.session_state.df
        summary = get_dataset_summary(df)

        st.divider()
        st.subheader("Dataset Overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rows", f"{summary['rows']:,}")
        col2.metric("Total Columns", summary["columns"])
        col3.metric("Numeric Columns", len(summary["numeric_cols"]))
        col4.metric("Missing Values", sum(summary["missing_values"].values()))

        st.divider()

        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("Data Preview")
            n_rows = st.slider("Number of rows to show", min_value=5, max_value=50, value=10)
            st.dataframe(df.head(n_rows), use_container_width=True)

        with col_right:
            st.subheader("Column Details")
            col_info = pd.DataFrame({
                "Column": df.columns,
                "Data Type": df.dtypes.values.astype(str),
                "Non-Null Count": df.count().values,
                "Null Count": df.isnull().sum().values
            })
            st.dataframe(col_info, use_container_width=True, height=400)

        st.divider()

        duplicate_count = summary["duplicates"]
        if duplicate_count > 0:
            st.warning(f"Found {duplicate_count} duplicate rows in the dataset.")
        else:
            st.success("No duplicate rows found.")

    else:
        st.info("Please upload a file above to continue.")