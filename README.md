# RAG Chatbot — Chat with your PDF using Groq + ChromaDB

A fast, lightweight RAG (Retrieval Augmented Generation) chatbot that lets you upload any PDF and ask questions about it. Built with FastAPI, ChromaDB, and Groq's Llama3 model.

---

## 🛠️ Tech Stack

- **FastAPI** — Backend API
- **ChromaDB** — Vector database (runs locally)
- **Groq (Llama3)** — AI answers
- **pdfplumber** — PDF text extraction
- **HTML/CSS/JS** — Frontend UI

---

## ⚙️ Prerequisites

- Python 3.10 or above
- A free Groq API key → [console.groq.com](https://console.groq.com)

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/rag-chatbot.git
cd rag-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

GROQ_API_KEY=your_groq_api_key_here

Replace `your_groq_api_key_here` with your actual key from [console.groq.com](https://console.groq.com)

### 6. Run the app

```bash
uvicorn main:app --reload
```

### 7. Open in browser
http://localhost:8000

---

## 💬 How to use

1. Upload any PDF using the sidebar
2. Wait for the **"X chunks ready"** confirmation
3. Ask anything about your PDF in the chat
4. Get AI-powered answers in real time ⚡

---

### 5. Set up environment variables

Create a `.env` file in the root of the project:
