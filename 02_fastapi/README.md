# ⚡ 02 — FastAPI

Learning FastAPI through the **"FastAPI - The Complete Course 2026"** on Udemy.

---

## 📚 What is FastAPI?
FastAPI is a modern Python web framework for building RESTful APIs.  
It's the **industry standard for AI/ML model serving** — used heavily in production AI systems.

**Why it matters for AI roles:**
- Serve ML model predictions as REST endpoints
- Used in nearly every LLM API backend
- Async-first = handles high concurrency for AI workloads

---

## 📖 Course Progress

| Section | Topic | Status |
|---------|-------|--------|
| Section 1 | Introduction | ✅ Done |
| Section 2 | Python Refresher | ✅ Done |
| Section 3 | FastAPI Overview | ✅ Done |
| Section 4 | FastAPI Setup & Installation | ✅ Done |
| Section 5 | Project 1 — Books API (Request Methods) | 🔄 In Progress |

---

## 📁 Structure

```
02_fastapi/
│
├── intro_to_fastapi.ipynb      # Concept notes
│
└── books_project/              # Section 5 — hands-on project
    ├── main.py                 # FastAPI app
    ├── requirements.txt
    └── README.md
```

---

## 🔑 Key Concepts Learned

- **GET / POST / PUT / DELETE** — HTTP request methods
- **Path Parameters** — dynamic URL segments (`/items/{id}`)
- **Query Parameters** — filters via URL (`/items?skip=0&limit=10`)
- **Request Body** — accepting JSON data from clients
- **Pydantic Models** — data validation built into FastAPI

---

## 🚀 How to Run the Books Project

```bash
cd books_project
pip install -r requirements.txt
uvicorn main:app --reload
```

Then open: `http://127.0.0.1:8000/docs` — FastAPI auto-generates interactive API docs ✨
