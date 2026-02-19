import pandas as pd
import numpy as np


def load_dataset(uploaded_file):
    """Load CSV or XLSX file into a DataFrame."""
    name = uploaded_file.name.lower()
    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload CSV or XLSX.")
    return df


def standardize_columns(df):
    """Standardize column names: strip, lowercase, replace spaces with underscores."""
    df = df.copy()
    df.columns = [c.strip().lower().replace(" ", "_").replace("-", "_") for c in df.columns]
    return df


def auto_detect_dates(df):
    """Try to parse object columns that look like dates."""
    df = df.copy()
    for col in df.select_dtypes(include="object").columns:
        try:
            converted = pd.to_datetime(df[col], infer_datetime_format=True)
            if converted.notna().sum() / len(df) > 0.7:
                df[col] = converted
        except Exception:
            pass
    return df


def handle_missing_values(df, strategy="none"):
    """
    Handle missing values for all column types.
    strategy: 'none', 'drop_rows', 'drop_high_missing_cols', 'fill_mean', 'fill_median', 'fill_mode'
    """
    df = df.copy()

    if strategy == "none":
        pass

    elif strategy == "drop_rows":
        # Only drop rows where numeric columns have missing values
        # For text columns with too many missing values, drop the column instead
        for col in df.select_dtypes(include="object").columns:
            missing_pct = df[col].isnull().sum() / len(df)
            if missing_pct > 0.5:
                df = df.drop(columns=[col])
        df = df.dropna()

    elif strategy == "drop_high_missing_cols":
        # Drop any column that has more than 40% missing values
        threshold = 0.4
        for col in df.columns:
            missing_pct = df[col].isnull().sum() / len(df)
            if missing_pct > threshold:
                df = df.drop(columns=[col])

    elif strategy == "fill_mean":
        # Fill numeric columns with mean
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].mean())
        # Fill text columns with mode
        for col in df.select_dtypes(include="object").columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    elif strategy == "fill_median":
        # Fill numeric columns with median
        for col in df.select_dtypes(include=np.number).columns:
            df[col] = df[col].fillna(df[col].median())
        # Fill text columns with mode
        for col in df.select_dtypes(include="object").columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    elif strategy == "fill_mode":
        # Fill all columns with their most frequent value
        for col in df.columns:
            if not df[col].mode().empty:
                df[col] = df[col].fillna(df[col].mode()[0])

    return df


def detect_outliers_iqr(df):
    """Return a dict mapping numeric column names to outlier counts using IQR."""
    outlier_info = {}
    for col in df.select_dtypes(include=np.number).columns:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR
        count = int(((df[col] < lower) | (df[col] > upper)).sum())
        outlier_info[col] = count
    return outlier_info


def get_dataset_summary(df):
    """Return a dict of basic summary info about the dataset."""
    return {
        "rows": len(df),
        "columns": len(df.columns),
        "numeric_cols": list(df.select_dtypes(include=np.number).columns),
        "categorical_cols": list(df.select_dtypes(include="object").columns),
        "date_cols": list(df.select_dtypes(include=["datetime64"]).columns),
        "missing_values": df.isnull().sum().to_dict(),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "duplicates": int(df.duplicated().sum()),
    }


def prepare_dataset(df, missing_strategy="none"):
    """Full pipeline: standardize → detect dates → handle missing."""
    df = standardize_columns(df)
    df = auto_detect_dates(df)
    df = handle_missing_values(df, strategy=missing_strategy)
    return df