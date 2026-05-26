# 🎓 Apex Coaching AI Assistant — Intelligent RAG Concierge

> An enterprise-grade conversational AI designed to handle admissions, courses, fees, and batch schedules. No generic UI footprints. Just a hyper-tailored, responsive assistant experience.

![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-LCEL-green?style=flat-square)
![FAISS](https://img.shields.io/badge/FAISS-VectorStore-orange?style=flat-square)
![Groq](https://img.shields.io/badge/Groq-LLM-orange?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-Cloud-red?style=flat-square&logo=streamlit)

---

## 🧠 What is Apex AI Assistant?

Apex AI Assistant is a production-ready **Retrieval-Augmented Generation (RAG)** system powered by an optimized LangChain LCEL pipeline. Built specifically for coaching institutes, it eliminates the generic and blocky look of standard AI tools — using a completely custom interface that blends seamlessly into institutional workflows.

```
"Admissions open kabse hain?"   → Context Retrieval → "Class 11/12 batch targets launch from..."
"NEET ki fees kya hai?"         → Semantic Search   → "The structure for premium batches is..."
"Batch timings kya hain?"       → Vector Extraction → "Morning shifts operate between 8AM - 12PM..."
```

The system ingests official FAQs, processes them into high-dimensional vector embeddings, handles vector search through **FAISS**, and streams responses with a dynamic animated typing workflow — all in one conversational turn.

---

## 🏗️ Architecture

```
User Input (Natural Language / Quick Chips)
        ↓
  Streamlit Custom Frontend
        ↓
  LangChain LCEL RAG Chain (Groq LLM)
        ↓
  FAISS Local Vector Index
        ↓
  Context-Aware Response + Metadata Styling
```

---

## ✨ Features

- 💬 **Bespoke HTML/CSS Interface** — Completely custom chat bubbles, proper user-right and bot-left alignments, and clean high-contrast text rendering
- 🎨 **Warm Cream Premium Aesthetic** — Custom-engineered theme with a Warm Cream `#FFFBF5` palette and Amber/Orange highlights
- 🧠 **Conversational Memory** — Full session-state message tracking (`HumanMessage` & `AIMessage`) for multi-turn academic consultations
- ⚡ **Hyper-Fast Inference** — Sub-second response token deliveries with live dynamic animated wave typing indicators
- 🛠️ **Lead Generation Module** — Fully integrated interactive sidebar for instant free demo seat bookings
- 🛡️ **Zero Ghost Wrappers** — Zero dependency on default Streamlit layout blocks, ensuring fully functional native window vertical scrolling

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM Engine | Groq (LLaMA Architecture) |
| RAG Framework | LangChain Expression Language (LCEL) |
| Vector Store | FAISS (Facebook AI Similarity Search) |
| Embeddings Model | HuggingFace (`all-MiniLM-L6-v2`) |
| Frontend | Streamlit with Forced Inline CSS Overrides |
| Environment | Python `dotenv` |

---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/kkc0de/apex-coaching-chatbot.git
cd apex-coaching-chatbot
```

### 2. Create a virtual environment
```bash
python -m venv venv
.\venv\Scripts\activate   # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root folder:
```env
GROQ_API_KEY=your-groq-api-key
```

### 5. Run the app
```bash
streamlit run app.py
```

---

## 🔍 RAG Pipeline Design

The knowledge retrieval is engineered in **three stages**:

1. **Ingestion** — Raw FAQ text is loaded and split into optimized chunks using LangChain's document loaders and text splitters
2. **Embedding** — Chunks are encoded into dense vectors using HuggingFace's `all-MiniLM-L6-v2` model and indexed into a local FAISS store
3. **Retrieval & Generation** — At query time, the top-k semantically similar chunks are retrieved and passed as context to the Groq LLM via an LCEL chain, producing grounded, hallucination-resistant answers

---

## 📁 Project Structure

```
apex-coaching-chatbot/
├── data/
│   └── coaching_faq.txt     # Raw institutional knowledge base
├── src/
│   ├── __init__.py
│   ├── chain.py             # LangChain LCEL RAG pipeline setup
│   ├── embedder.py          # FAISS indexing and vector store managers
│   └── loader.py            # Text document splitting & loading algorithms
├── .env                     # Environment configurations (API keys)
├── .gitignore               # Excludes production keys and environment tracks
├── app.py                   # Main UI shell & custom DOM overrides
├── requirements.txt         # Project runtime dependencies
└── README.md
```

---

## 🌐 Live Demo

> 🔗 https://apex-coaching-chatbot-tzszranyqc4kddnqdkonqs.streamlit.app/

---

## 📄 License

MIT License — feel free to fork and build your own custom-styled RAG solutions.

---

<p align="center">Built by <a href="https://www.linkedin.com/in/krishna-sharma-veltr0/">Veltro</a></p>
