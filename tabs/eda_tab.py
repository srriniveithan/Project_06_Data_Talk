import streamlit as st
import numpy as np
import pandas as pd
from data_prep import detect_outliers_iqr
from eda import (
    descriptive_statistics,
    missing_values_report,
    plot_correlation_heatmap,
    plot_distributions,
    plot_categorical_counts,
    plot_missing_values,
    plot_outliers_boxplot,
)


def render():
    st.title("📊 EDA Dashboard")

    if st.session_state.df is None:
        st.info("Please upload a dataset first.")
        return

    df = st.session_state.df

    eda1, eda2, eda3, eda4, eda5 = st.tabs([
        "Statistics",
        "Correlation",
        "Distributions",
        "Categories",
        "Outliers"
    ])

    # --- Statistics ---
    with eda1:
        st.subheader("Descriptive Statistics")
        stats = descriptive_statistics(df)
        if not stats.empty:
            st.dataframe(stats, use_container_width=True)
        else:
            st.info("No numeric columns found in this dataset.")

        st.divider()
        st.subheader("Missing Values")
        mv = missing_values_report(df)
        if not mv.empty:
            st.dataframe(mv, use_container_width=True)
            chart = plot_missing_values(df)
            if chart:
                st.image(chart)
        else:
            st.success("Great! No missing values found.")

    # --- Correlation ---
    with eda2:
        st.subheader("Correlation Heatmap")
        st.write("Shows how numeric columns are related to each other.")
        chart = plot_correlation_heatmap(df)
        if chart:
            st.image(chart, use_container_width=True)
        else:
            st.info("Need at least 2 numeric columns to show correlation.")

    # --- Distributions ---
    with eda3:
        st.subheader("Numeric Column Distributions")
        num_cols = df.select_dtypes(include=np.number).columns.tolist()

        if num_cols:
            selected = st.multiselect(
                "Select columns to view",
                options=num_cols,
                default=num_cols[:min(6, len(num_cols))]
            )
            if selected:
                chart = plot_distributions(df[selected])
                if chart:
                    st.image(chart, use_container_width=True)
        else:
            st.info("No numeric columns available.")

    # --- Categories ---
    with eda4:
        st.subheader("Categorical Column Counts")
        cat_cols = df.select_dtypes(include="object").columns.tolist()

        if cat_cols:
            selected_cat = st.multiselect(
                "Select columns to view",
                options=cat_cols,
                default=cat_cols[:min(4, len(cat_cols))]
            )
            if selected_cat:
                chart = plot_categorical_counts(df[selected_cat])
                if chart:
                    st.image(chart, use_container_width=True)
        else:
            st.info("No categorical columns available.")

    # --- Outliers ---
    with eda5:
        st.subheader("Outlier Detection using IQR Method")
        outliers = detect_outliers_iqr(df)

        if outliers:
            outlier_df = pd.DataFrame(
                list(outliers.items()),
                columns=["Column", "Outlier Count"]
            ).sort_values("Outlier Count", ascending=False)

            st.dataframe(outlier_df, use_container_width=True)

            st.divider()
            st.subheader("Boxplots")
            chart = plot_outliers_boxplot(df)
            if chart:
                st.image(chart, use_container_width=True)
        else:
            st.info("No numeric columns to check for outliers.")