# 💬 DataTalk — Conversational Data Analysis & Auto-Visualization System

A Streamlit-based intelligent analytics app that lets you **upload data, explore it visually, and chat with it using natural language** — powered by Groq LLM (Llama 3).

---

## 🚀 Features

- 📂 **Smart Data Upload** — CSV & XLSX with auto type detection & column standardization
- 🧹 **Data Preparation** — Missing value handling, outlier detection (IQR), date detection
- 📊 **Automated EDA Dashboard** — Stats, correlation heatmap, distributions, outlier boxplots
- 💬 **Chat with Data** — Ask natural language questions, get answers + auto-generated charts
- 📈 **Auto Visualization Engine** — Smart chart selection (bar, line, scatter, histogram, boxplot, pie)
- ⬇️ **Downloadable Charts** — Export any chart as PNG

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend UI | Streamlit |
| LLM | Groq (Llama 3 70B / 8B, Mixtral, Gemma) |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/datatalk.git
cd datatalk
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a Free Groq API Key
- Visit https://console.groq.com
- Sign up and create an API key

### 4. Run the app
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
datatalk/
├── app.py              # Main Streamlit application
├── data_prep.py        # Data loading, cleaning & preparation
├── eda.py              # EDA plots and statistics
├── viz_engine.py       # Auto-visualization engine
├── llm_engine.py       # Groq LLM integration & chat engine
├── requirements.txt    # Python dependencies
└── README.md
```

---

## 💡 Example Questions to Ask

| Category | Example |
|----------|---------|
| Descriptive | "What is the average revenue?" |
| Trend | "Show monthly sales trend" |
| Comparison | "Which region has the highest profit?" |
| Visualization | "Plot age distribution" |
| Data Quality | "Which columns have missing values?" |

---

## 🌐 Deployment

**Streamlit Cloud** (recommended):
1. Push code to GitHub
2. Go to share.streamlit.io
3. Connect your repo and deploy

Other: Render, Railway, AWS, GCP, Azure

---

*Built as a capstone project for GUVI | HCL Data Science Program*
