import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

PALETTE = "muted"
FIG_DPI = 120


def _fig_to_bytes(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=FIG_DPI)
    buf.seek(0)
    plt.close(fig)
    return buf


def infer_best_chart(df, x_col, y_col=None, question=""):
    """Infer the best chart type based on data types and optional question text."""
    q = question.lower()
    x_dtype = df[x_col].dtype

    # Question-based hints
    if any(w in q for w in ["distribution", "histogram", "dist"]):
        return "histogram"
    if any(w in q for w in ["scatter", "vs", "versus", "correlation between"]):
        return "scatter"
    if any(w in q for w in ["trend", "over time", "monthly", "yearly", "time"]):
        return "line"
    if any(w in q for w in ["pie", "proportion", "share", "percentage"]):
        return "pie"
    if any(w in q for w in ["box", "outlier", "spread"]):
        return "boxplot"

    # Data-type based inference
    if y_col is None:
        if pd.api.types.is_numeric_dtype(x_dtype):
            return "histogram"
        else:
            return "bar"

    y_dtype = df[y_col].dtype
    if pd.api.types.is_datetime64_any_dtype(x_dtype):
        return "line"
    if pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
        return "scatter"
    if not pd.api.types.is_numeric_dtype(x_dtype) and pd.api.types.is_numeric_dtype(y_dtype):
        return "bar"
    return "bar"


def render_chart(df, chart_type, x_col, y_col=None, agg_func="mean", title=""):
    """Render a chart and return as bytes."""
    fig, ax = plt.subplots(figsize=(10, 5))

    try:
        if chart_type == "histogram":
            col = x_col
            sns.histplot(df[col].dropna(), kde=True, ax=ax,
                         color=sns.color_palette(PALETTE)[0])
            ax.set_xlabel(col)
            ax.set_title(title or f"Distribution of {col}")

        elif chart_type == "bar":
            if y_col:
                agg = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
                agg = agg.sort_values(y_col, ascending=False).head(20)
                sns.barplot(data=agg, x=x_col, y=y_col, ax=ax, palette=PALETTE)
                ax.set_title(title or f"{agg_func.title()} of {y_col} by {x_col}")
                plt.xticks(rotation=45, ha="right")
            else:
                counts = df[x_col].value_counts().head(20)
                sns.barplot(x=counts.index, y=counts.values, ax=ax, palette=PALETTE)
                ax.set_title(title or f"Count of {x_col}")
                plt.xticks(rotation=45, ha="right")

        elif chart_type == "line":
            if y_col:
                agg = df.groupby(x_col)[y_col].agg(agg_func).reset_index()
                ax.plot(agg[x_col], agg[y_col], marker="o", color=sns.color_palette(PALETTE)[0])
                ax.set_xlabel(x_col)
                ax.set_ylabel(y_col)
                ax.set_title(title or f"{y_col} Trend over {x_col}")
                plt.xticks(rotation=45, ha="right")
            else:
                counts = df[x_col].value_counts().sort_index()
                ax.plot(counts.index, counts.values, marker="o")
                ax.set_title(title or f"{x_col} over time")
                plt.xticks(rotation=45, ha="right")

        elif chart_type == "scatter":
            if y_col:
                sns.scatterplot(data=df, x=x_col, y=y_col, ax=ax,
                                alpha=0.6, palette=PALETTE)
                ax.set_title(title or f"{x_col} vs {y_col}")
            else:
                ax.text(0.5, 0.5, "Please select a Y-axis column for scatter plot",
                        ha="center", va="center", transform=ax.transAxes)

        elif chart_type == "pie":
            col = y_col if y_col else x_col
            group_col = x_col
            if y_col:
                data = df.groupby(group_col)[col].agg(agg_func)
            else:
                data = df[group_col].value_counts()
            data = data.head(10)
            ax.pie(data.values, labels=data.index, autopct="%1.1f%%",
                   colors=sns.color_palette(PALETTE, len(data)))
            ax.set_title(title or f"Proportion of {col}")

        elif chart_type == "boxplot":
            if y_col and not pd.api.types.is_numeric_dtype(df[x_col]):
                top_cats = df[x_col].value_counts().head(10).index
                plot_df = df[df[x_col].isin(top_cats)]
                sns.boxplot(data=plot_df, x=x_col, y=y_col, ax=ax, palette=PALETTE)
                ax.set_title(title or f"Distribution of {y_col} by {x_col}")
                plt.xticks(rotation=45, ha="right")
            else:
                col = y_col if y_col else x_col
                sns.boxplot(y=df[col].dropna(), ax=ax, color=sns.color_palette(PALETTE)[0])
                ax.set_title(title or f"Box Plot of {col}")

        plt.tight_layout()
        return _fig_to_bytes(fig)

    except Exception as e:
        plt.close(fig)
        raise e
