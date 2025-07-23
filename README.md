# 🕸️ WebScraper AI Agent

An AI-powered web scraper that extracts and processes website data using LangChain, HuggingFace embeddings, FAISS, and GROQ LLMs. Built with Gradio for a simple UI interface.

---

## 🚀 Features

- 🌐 Crawl websites asynchronously with `Crawl4AI`
- 📄 Extract and chunk website text data
- 🤖 Embed content using `HuggingFaceEmbeddings`
- 🔍 Perform semantic search using `FAISS`
- 💬 Answer questions using GROQ LLM (via LangChain)
- 🎛️ Clean and interactive UI using `Gradio`

---

## 🧰 Tech Stack

- Python
- LangChain
- FAISS
- HuggingFace Transformers
- Crawl4AI
- Gradio
- GROQ LLM
- dotenv

---

## 📦 Installation

```bash
git clone https://github.com/jasoncobra3/WebScraper_AI_Agent.git
cd WebScraper_AI_Agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
---
## 🔐 Setup
1. Create a .env file
   ```env
    GROQ_API_KEY=your_groq_api_key_here
   ```
2.  Replace the `.env.`example if needed.
---

##  🧪Run the App
   ```bash
     python app.py
   ```

---

## 📁 Project Structure
```
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── crawl4ai/  # Library or module
```
---
## 📸 Screenshots

| 🌐 Scraping Website|Semantic Search 📄 |
|---------------|------------------|
| ![Scrape](Assets/screenshot1.png) | ![Semantic_Search](Assets/screenshot2.png)|

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you’d like to change.

