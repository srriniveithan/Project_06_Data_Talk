import os
import pandas as pd
import numpy as np
import traceback
from groq import Groq


def get_groq_client(api_key: str):
    return Groq(api_key=api_key)


def build_system_prompt(df: pd.DataFrame) -> str:
    """Build a system prompt with dataset context."""
    num_cols = df.select_dtypes(include=np.number).columns.tolist()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    date_cols = df.select_dtypes(include=["datetime64"]).columns.tolist()

    sample = df.head(3).to_string(index=False)

    prompt = f"""You are DataTalk, an expert data analyst AI assistant. 
You are analyzing a dataset with the following properties:

SHAPE: {df.shape[0]} rows × {df.shape[1]} columns
COLUMNS: {list(df.columns)}
NUMERIC COLUMNS: {num_cols}
CATEGORICAL COLUMNS: {cat_cols}
DATE COLUMNS: {date_cols}

SAMPLE DATA (first 3 rows):
{sample}

MISSING VALUES: {df.isnull().sum().to_dict()}

BASIC STATS:
{df.describe(include='all').to_string()}

Your job is to:
1. Answer the user's question about this dataset clearly and concisely.
2. If the question requires computation, provide the Python/Pandas code snippet to compute it (inside ```python ... ``` blocks).
3. If a visualization would help, specify it in the format: CHART:<chart_type>|X:<x_col>|Y:<y_col>
   - chart_type: bar, line, scatter, histogram, pie, boxplot
   - Example: CHART:bar|X:region|Y:revenue
4. Provide insights and interpretations, not just raw numbers.
5. Keep your response concise and business-friendly.

Rules:
- ALWAYS reference actual column names from the dataset.
- If a column doesn't exist, say so clearly.
- If you generate Python code, use `df` as the dataframe variable.
- Do not make up data that isn't in the dataset.
"""
    return prompt


def execute_pandas_code(df: pd.DataFrame, code: str):
    """Safely execute pandas code and return result."""
    local_vars = {"df": df.copy(), "pd": pd, "np": np}
    try:
        exec(code, {"__builtins__": {}}, local_vars)
        result = local_vars.get("result", None)
        return result, None
    except Exception as e:
        return None, str(e)


def parse_chart_instruction(response_text: str):
    """Extract chart instruction from LLM response if present."""
    import re
    pattern = r"CHART:(\w+)\|X:(\w+)(?:\|Y:(\w+))?"
    match = re.search(pattern, response_text)
    if match:
        chart_type = match.group(1)
        x_col = match.group(2)
        y_col = match.group(3)
        return {"chart_type": chart_type, "x_col": x_col, "y_col": y_col}
    return None


def extract_code_blocks(text: str):
    """Extract all python code blocks from LLM response."""
    import re
    pattern = r"```python\s*(.*?)```"
    return re.findall(pattern, text, re.DOTALL)


def chat_with_data(
    df: pd.DataFrame,
    user_question: str,
    chat_history: list,
    api_key: str,
    model: str = "llama-3.3-70b-versatile",
):
    """
    Send user question to Groq LLM with dataset context.
    Returns: (assistant_reply, chart_instruction_dict_or_None, code_result_or_None, error_or_None)
    """
    client = get_groq_client(api_key)

    messages = [{"role": "system", "content": build_system_prompt(df)}]
    for msg in chat_history[-6:]:  # keep last 6 messages for context window
        messages.append(msg)
    messages.append({"role": "user", "content": user_question})

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.3,
            max_tokens=1500,
        )
        reply = response.choices[0].message.content

        # Try to execute any code blocks
        code_result = None
        code_error = None
        codes = extract_code_blocks(reply)
        if codes:
            code_result, code_error = execute_pandas_code(df, codes[0])

        # Parse chart instructions
        chart_instruction = parse_chart_instruction(reply)

        return reply, chart_instruction, code_result, code_error

    except Exception as e:
        error_msg = str(e)
        if "decommissioned" in error_msg or "model" in error_msg.lower():
            return None, None, None, "This model has been decommissioned. Please select llama-3.3-70b-versatile from the sidebar."
        elif "401" in error_msg or "api_key" in error_msg.lower():
            return None, None, None, "Invalid API key. Please check your Groq API key in the sidebar."
        elif "429" in error_msg:
            return None, None, None, "Rate limit reached. Please wait a moment and try again."
        else:
            return None, None, None, error_msg