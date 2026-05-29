# 📚 Books API — FastAPI Project 1

A REST API for managing a books collection, built while learning FastAPI fundamentals.  
Covers all **CRUD operations** using proper HTTP request methods.

---

## 🚀 What it does

| Operation | HTTP Method | Endpoint | Description |
|-----------|-------------|----------|-------------|
| Read all | `GET` | `/books` | Fetch all books |
| Read one | `GET` | `/books/{title}` | Fetch a book by title |
| Read by category | `GET` | `/books/?category=science` | Filter books by category |
| Create | `POST` | `/books` | Add a new book |
| Update | `PUT` | `/books/{title}` | Edit an existing book |
| Delete | `DELETE` | `/books/{title}` | Remove a book |

---

## 📦 Data Structure

Each book is a key-value object:

```json
{
  "title": "The Great Gatsby",
  "author": "F. Scott Fitzgerald",
  "category": "fiction"
}
```

---

## ⚙️ How to Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
uvicorn main:app --reload

# 3. Open interactive docs
# http://127.0.0.1:8000/docs
```

---

## 🗂️ Project Structure

```
books_project/
├── main.py              # FastAPI app — all routes and logic
├── requirements.txt     # fastapi, uvicorn
└── README.md
```

---

## 💡 Concepts Practiced

- `@app.get` / `@app.post` / `@app.put` / `@app.delete` decorators
- **Path parameters** — `/books/{title}`
- **Query parameters** — `/books/?category=science`
- **Request body** — accepting JSON data via POST
- FastAPI auto-generated **Swagger UI** at `/docs`

---

*Project from Section 5 — FastAPI The Complete Course 2026*
