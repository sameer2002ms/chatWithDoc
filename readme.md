# 📄 RAG-based Document Question Answering System

### Version 1 of the project focused on building a minimal production-style RAG pipeline using Django, OpenAI embeddings, and Qdrant.

---

## 🚀 Features

* 📄 PDF ingestion (in-memory)
* ✂️ Token-based chunking with overlap
* 🧠 OpenAI embeddings (`text-embedding-3-small`)
* 📦 Vector storage using QdrantDB
* 🔍 Semantic retrieval scoped to the latest document
* 🤖 GPT-based grounded answer generation
* 🛡️ Hallucination-controlled prompts
* 💸 Cost-optimized retrieval and generation
* 🐳 Fully Dockerized setup

---

## 🏗️ Architecture Overview

```
Client
 └──> Django REST API
        ├── /api/ingest  (PDF upload)
        ├── Chunking + Embeddings
        ├── Qdrant Vector Store
        └── /api/ask     (Question Answering)
               ├── Retrieval (Qdrant)
               └── GPT Answer Generation
```

---

## 🛠️ Tech Stack

### Backend

* Python 3.11
* Django
* Django REST Framework

### GenAI

* OpenAI API

  * text-embedding-3-small
  * gpt-4.1-mini

### Vector Database

* Qdrant

### Infrastructure

* Docker & Docker Compose
* PostgreSQL (document metadata)

---

## ⚙️ Prerequisites

* Docker
* Docker Compose
* OpenAI API Key

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
OPENAI_CHAT_MODEL=gpt-4.1-mini
```

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

### 2️⃣ Start Services Using Docker

```bash
docker-compose up --build
```

This will start:

* Django backend (`http://localhost:8000`)
* PostgreSQL
* Qdrant (`http://localhost:6333/dashboard`)

---

### 3️⃣ Apply Database Migrations

```bash
docker exec -it rag_backend bash
python manage.py migrate
```

---

## 📤 API Usage

### 🔹 1. Ingest PDF

**Endpoint**

```
POST /api/ingest/
```

**Request**

* `multipart/form-data`
* Field: `files` (PDF)

**Response**

```json
{
  "documents": [
    {
      "filename": "resume.pdf",
      "document_id": "uuid",
      "status": "INGESTED",
      "chunk_count": 2
    }
  ]
}
```

---

### 🔹 2. Ask Question

**Endpoint**

```
POST /api/ask/
```

**Request Body**

```json
{
  "question": "What technologies does the candidate know?",
  "top_k": 3
}
```

**Response**

```json
{
  "answer": "The candidate has experience with Python, Django, Azure Functions, Docker, and React.",
  "sources": [
    {
      "chunk_index": 0,
      "score": 0.31
    }
  ]
}
```

---

## 🧠 Key Design Decisions (Interview Ready)

* **PostgreSQL as source of truth** – tracks document lifecycle and metadata
* **Qdrant only for vector search** – never treated as primary storage
* **Token-based chunking with overlap** – preserves semantic continuity
* **Score-based chunk filtering** – reduces hallucination and cost
* **Grounded prompting** – GPT answers only from retrieved context
* **Low temperature generation** – factual, deterministic answers

---

## 💰 Cost Optimization

* Embeddings are generated **once per document**
* GPT is called **only after retrieval**
* Context size is controlled via `top_k` and similarity score threshold
* Typical cost per question: **~$0.00008**

🧮 TOTAL COST BREAKDOWN (Realistic)

**Action**	                     **Cost**
Upload 1 resume (embedding)	~$0.00001
Ask    1 question	        ~$0.00008
Ask    100 questions	    ~$0.008
Ask    1,000 questions	    ~$0.08
Ask    10,000 questions     ~$0.80

---

## 🧪 Development Notes

* Retrieval is currently scoped to the **latest uploaded document**
* Easy to extend to multi-document search, conversation memory, streaming answers, and frontend UI

---

## Advanced Version (V2)

This repository is the upgraded evolution of the original RAG backend project:

➡️ https://github.com/sameer2002ms/chatWithDoc-using-Langchain

Enhancements introduced in V2:

* LangChain Runnable-based architecture
* Multi-format ingestion support

  * PDF
  * DOCX
  * HTML
  * Public URLs
* Metadata-scoped retrieval in Qdrant
* Improved modular backend structure
* Better scalability and maintainability
* Enhanced grounded answer generation pipeline
* More production-oriented RAG workflow

---

## 👨‍💻 Author
**Mohd Sameer Backend developer at IBM**

Built as a **resume-grade GenAI system** with a focus on clean backend architecture, explainability, cost efficiency, and interview readiness.



