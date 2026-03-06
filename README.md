# 🔍 ComplianceIQ — RAG-Powered Compliance Document Assistant

An AI-powered compliance assistant that lets you ask natural language questions over official SOC 2 Trust Services Criteria documents and get accurate, source-cited answers in seconds.

Built with LangChain, FAISS, and `openai/gpt-oss-120b` via Groq.

---

## 📌 What It Does

- Ingests the official **AICPA SOC 2 Trust Services Criteria (TSP Section 100, 2022)** PDF
- Chunks and embeds the document using `sentence-transformers/all-MiniLM-L6-v2`
- Stores embeddings locally using **FAISS** (no cloud vector DB needed)
- On each question, retrieves the most relevant chunks and passes them to the LLM
- Returns a **grounded answer** with **source filename and page number** citations

---

## 🧠 How the RAG Pipeline Works

```
PDF Document
     ↓
PyPDFLoader (page-by-page loading with metadata)
     ↓
RecursiveCharacterTextSplitter (chunk_size=1000, overlap=100)
     ↓
HuggingFace Embeddings (all-MiniLM-L6-v2) → stored in FAISS locally
     ↓
User asks a question via Streamlit UI
     ↓
FAISS retrieves top-4 relevant chunks
     ↓
Chunks + question passed to openai/gpt-oss-120b via Groq API
     ↓
Answer generated + source page citations displayed
```

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| LLM | `openai/gpt-oss-120b` via Groq API |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (HuggingFace) |
| Vector Store | FAISS (local) |
| RAG Framework | LangChain |
| PDF Loader | PyPDFLoader (LangChain Community) |
| UI | Streamlit |
| Backend | Python |

---

## 📁 Project Structure

```
ComplianceIQ/
│
├── data/
│   └── AICPA-TSP-Section-100-Trust-Services-Criteria-2022.pdf
│
├── faiss_index/              ← auto-created after running ingest.py
│   ├── index.faiss
│   └── index.pkl
│
├── ingest.py                 ← loads PDF, creates embeddings, saves FAISS index
├── rag_chain.py              ← retrieval chain, returns answer + source citations
├── app.py                    ← Streamlit UI
├── requirements.txt
├── .env                      ← store your GROQ_API_KEY here
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.10+
- A Groq API key → get one free at [console.groq.com](https://console.groq.com)

### Step 1 — Clone and set up environment

```bash
git clone https://github.com/yourusername/ComplianceIQ.git
cd ComplianceIQ

python -m venv my_env
my_env\Scripts\activate       # Windows
source my_env/bin/activate    # Mac/Linux

pip install -r requirements.txt
```

### Step 2 — Add your API key

Create a `.env` file in the root folder:

```
GROQ_API_KEY="your_groq_api_key_here"
```

### Step 3 — Run ingest (one time only)

```bash
python ingest.py
```

This loads the PDF, creates embeddings, and saves the FAISS index locally. You only need to run this once.

Expected output:
```
Loading PDF...
Loaded 74 pages. Splitting...
Created 480 chunks. Creating embeddings...
FAISS index saved to 'faiss_index'
```

### Step 4 — Launch the app

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 💬 Example Questions

| Question | Expected Pages |
|---|---|
| What is SOC 2 and who created it? | Page 2–3 |
| What are the five Trust Services Categories? | Page 6–8 |
| What is the difference between Confidentiality and Privacy? | Page 7–8 |
| What does CC6.1 require for logical access controls? | Page 33–34 |
| How should an organization respond to a security incident? | Page 41–43 |
| What are the Privacy criteria related to Notice and Communication? | Page 55–57 |
| What does Processing Integrity mean? | Page 7–8, 52–54 |

---

## 📄 Source Document

**2017 Trust Services Criteria for Security, Availability, Processing Integrity, Confidentiality, and Privacy (With Revised Points of Focus — 2022)**
Published by: American Institute of Certified Public Accountants (AICPA)
Document: TSP Section 100

---

## ⚠️ Disclaimer

This tool is for informational and educational purposes only. It is not a substitute for professional compliance advice or a formal SOC 2 audit. Always consult a qualified auditor for compliance decisions.

---

## 👤 Author

**Ishan Naikele**
AI/ML Engineer  
