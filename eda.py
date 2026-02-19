import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import io


# ── Palette / style helpers ──────────────────────────────────────────────────
PALETTE = "muted"
FIG_DPI = 120


def _fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=FIG_DPI)
    buf.seek(0)
    plt.close(fig)
    return buf


# ── Summary statistics ────────────────────────────────────────────────────────
def descriptive_statistics(df):
    num_df = df.select_dtypes(include=np.number)
    if num_df.empty:
        return pd.DataFrame()
    return num_df.describe().T.round(3)


def missing_values_report(df):
    missing = df.isnull().sum()
    pct = (missing / len(df) * 100).round(2)
    report = pd.DataFrame({"Missing Count": missing, "Missing %": pct})
    return report[report["Missing Count"] > 0].sort_values("Missing Count", ascending=False)


# ── Plots ─────────────────────────────────────────────────────────────────────
def plot_correlation_heatmap(df):
    num_df = df.select_dtypes(include=np.number)
    if num_df.shape[1] < 2:
        return None
    corr = num_df.corr()
    size = max(6, min(14, corr.shape[0]))
    fig, ax = plt.subplots(figsize=(size, size * 0.8))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        center=0,
        linewidths=0.5,
        ax=ax,
        annot_kws={"size": 8},
    )
    ax.set_title("Correlation Heatmap", fontsize=14, pad=12)
    plt.tight_layout()
    return _fig_to_bytes(fig)


def plot_distributions(df, max_cols=6):
    num_cols = df.select_dtypes(include=np.number).columns.tolist()[:max_cols]
    if not num_cols:
        return None
    n = len(num_cols)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = np.array(axes).flatten()
    for i, col in enumerate(num_cols):
        sns.histplot(df[col].dropna(), kde=True, ax=axes[i], color=sns.color_palette(PALETTE)[i % 6])
        axes[i].set_title(col, fontsize=10)
        axes[i].set_xlabel("")
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Column Distributions", fontsize=13, y=1.01)
    plt.tight_layout()
    return _fig_to_bytes(fig)


def plot_categorical_counts(df, max_cols=4, max_categories=15):
    cat_cols = df.select_dtypes(include="object").columns.tolist()[:max_cols]
    if not cat_cols:
        return None
    n = len(cat_cols)
    ncols = min(2, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(7 * ncols, 4 * nrows))
    axes = np.array(axes).flatten()
    for i, col in enumerate(cat_cols):
        top = df[col].value_counts().head(max_categories)
        sns.barplot(x=top.values, y=top.index, ax=axes[i], palette=PALETTE)
        axes[i].set_title(col, fontsize=10)
        axes[i].set_xlabel("Count")
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Categorical Column Counts", fontsize=13, y=1.01)
    plt.tight_layout()
    return _fig_to_bytes(fig)


def plot_missing_values(df):
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if missing.empty:
        return None
    fig, ax = plt.subplots(figsize=(8, max(3, len(missing) * 0.4 + 1)))
    colors = sns.color_palette("Reds_r", len(missing))
    missing.sort_values().plot(kind="barh", ax=ax, color=colors)
    ax.set_title("Missing Values per Column", fontsize=13)
    ax.set_xlabel("Count")
    plt.tight_layout()
    return _fig_to_bytes(fig)


def plot_outliers_boxplot(df, max_cols=6):
    num_cols = df.select_dtypes(include=np.number).columns.tolist()[:max_cols]
    if not num_cols:
        return None
    n = len(num_cols)
    ncols = min(3, n)
    nrows = (n + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(5 * ncols, 4 * nrows))
    axes = np.array(axes).flatten()
    for i, col in enumerate(num_cols):
        sns.boxplot(y=df[col].dropna(), ax=axes[i], color=sns.color_palette(PALETTE)[i % 6])
        axes[i].set_title(col, fontsize=10)
    for j in range(i + 1, len(axes)):
        axes[j].set_visible(False)
    fig.suptitle("Outlier Detection (Boxplots)", fontsize=13, y=1.01)
    plt.tight_layout()
    return _fig_to_bytes(fig)
