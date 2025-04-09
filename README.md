# 🧠 TRACE Professor Feedback Chatbot

A RAG-powered chatbot that answers student-style questions about professor feedback using TRACE survey data (PDFs) — with Chain-of-Thought reasoning, vector search using Pinecone, and a sleek Streamlit UI.

---

## 🚀 Features

- 🔍 PDF ingestion from GCP
- 📄 Text extraction & metadata parsing
- 🧼 Data cleaning + ratings/comments extraction
- 🛢️ PostgreSQL storage
- 🔗 Chunked + embedded using OpenAI (`text-embedding-3-small`)
- 🌲 Stored in Pinecone for fast vector retrieval
- 🧠 Chain-of-Thought prompting for enhanced semantic queries
- ✨ Final answer generated using OpenAI (GPT-3.5-Turbo or GPT-4)
- 💬 Streamlit-powered chat interface with animated response

---

## 📂 Project Structure

```
trace_rag_project/
│
├── main.py                    # Extract PDFs from GCP → Clean → Store in DB
├── run_embedding.py           # Chunk data → Embed using OpenAI → Store in Pinecone
├── rag_chain_of_thought.py   # Full RAG chatbot pipeline using CoT
├── app.py                     # Streamlit UI for chatting with the bot
│
├── config/
│   └── settings.py            # API keys, DB credentials, GCP config
│
├── gcs/
│   └── downloader.py          # Download PDFs from Google Cloud Storage
│
├── parser/
│   ├── pdf_text_extractor.py # Extract raw text using PyMuPDF
│   └── trace_cleaner.py       # Clean, parse ratings & comments
│
├── db/
│   ├── db_init.py             # Create tables in PostgreSQL
│   └── db_insert.py           # Insert processed data into DB
│
├── embedding/
│   ├── chunker.py             # Chunk full text + comments
│   ├── embedder.py            # Generate OpenAI embeddings
│   └── pinecone_uploader.py   # Upload chunks to Pinecone
```

---

## 🧪 How to Run

### 1. Install Requirements

```bash
pip install -r requirements.txt
```

### 2. Extract and Store PDF Data

```bash
python main.py
```

### 3. Embed and Upload to Pinecone

```bash
python run_embedding.py
```

### 4. Launch the Chatbot UI

```bash
streamlit run app.py
```

---

## 💬 Sample Questions to Ask

- What do students think about Tejas Parikh’s teaching style?
- How difficult were the assignments in this course?
- What kind of feedback did students give about inclusiveness?
- How well does this course prepare students for real-world roles?

---

## 🔐 Environment Setup

You’ll need:

- ✅ OpenAI API Key
- ✅ Pinecone API Key + environment (`us-east-1-aws`, etc.)
- ✅ PostgreSQL running locally (or in the cloud)
- ✅ GCP service account key (for reading PDFs)

Store your credentials in `config/settings.py` or load via `.env`.

---

## 📦 requirements.txt

```
openai==1.14.3
pinecone==3.0.0
python-dotenv==1.0.1
psycopg2-binary==2.9.9
PyMuPDF==1.23.7
google-cloud-storage==2.14.0
google-auth==2.29.0
streamlit==1.32.2
requests==2.31.0
```

---

## 🤝 Credits

Developed by Sai Manas and Logeshwaran   
Inspired by real-world professor feedback analysis needs using the TRACE system.

---

## 📬 Contact

Feel free to connect or reach out on [LinkedIn](#) | [GitHub](#) | [Email](#)

---

## 🧠 Future Improvements

- ✅ Show source PDF chunks alongside answers
- 🧠 Add re-ranking using GPT-4
- 🌐 Deploy to Streamlit Cloud or HuggingFace Spaces
- 🔒 Role-based access for admin/instructors
