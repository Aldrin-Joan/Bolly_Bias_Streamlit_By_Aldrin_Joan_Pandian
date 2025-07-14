# 🎬 BollyAI 2.0 – Bollywood Bias Buster

**BollyAI 2.0** is a powerful multimodal AI toolkit designed to detect and mitigate **gender stereotypes** in Bollywood media using Large Language Models (LLMs), Vision-Language Models, and structured analysis techniques.

> 🚀 Built using: `Streamlit`, `Transformers`, `Mistral`, `LLaVA`, `Matplotlib`, `Seaborn`

---

## ⚙️ Installation

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/BollyAI_web.git
cd BollyAI_web
```

### 2. Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

```bash
streamlit run app.py
```

Use the sidebar to navigate through each module.

---

## 🧩 Features

| Module                 | Description                                              |
|------------------------|----------------------------------------------------------|
| 📄 Data Cleaning       | Extract gender-tagged dialogues from scripts (PDF → CSV) |
| 🧠 Classification      | Detects gender stereotypes using local Mistral LLM       |
| 📊 Visualization       | Shows bias category distribution, gender-wise plots      |
| ✍️ Rewrite             | Rewrites biased lines using LLM guidance                 |
| 📁 Report Generation   | Generates downloadable PDF + CSV report                  |
| 🖼️ Poster Analysis     | Detects visual gender bias using LLaVA 1.5               |
| 🎞️ Trailer Analysis    | Plots emotion–gender patterns over time                  |
| 📚 Wikipedia Analytics | Adjective/verb usage, centrality, coreference, songs     |

---

## 🧠 Models Used

- 🤖 **Mistral-7B (GGUF)**
- 🧠 **LLaVA-1.5**
- 📈 **Matplotlib + Seaborn** — for plotting trailer and Wikipedia analytics
