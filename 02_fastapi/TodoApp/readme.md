# ✅ Todo Application

A full-stack Todo Management application built with **FastAPI**, featuring JWT authentication, role-based authorization, database migrations, unit testing, and cloud deployment.

This project was initially developed while learning FastAPI and has since been refactored using production-oriented backend engineering practices.

---

# 🚀 Live Demo

**Application:** *https://todoapp-deployment-aam4.onrender.com*



---

# ✨ Features

## Authentication

* User Registration
* Secure Login
* Logout
* JWT Authentication
* OAuth2 Password Flow
* Password Hashing using bcrypt

---

## Todo Management

* Create Todo
* View Todos
* Update Todo
* Delete Todo
* User-specific Todo Ownership
* Task Completion Status
* Priority Levels

---

## User Management

* View Profile
* Update Password
* Update Phone Number

---

## Admin Features

* View All Todos
* Delete Any Todo
* Role-Based Authorization

---

# 🛠 Technology Stack

| Category            | Technologies       |
| ------------------- | ------------------ |
| Backend             | FastAPI            |
| Database            | PostgreSQL, SQLite |
| ORM                 | SQLAlchemy         |
| Database Migrations | Alembic            |
| Authentication      | JWT, OAuth2        |
| Validation          | Pydantic           |
| Password Security   | Passlib (bcrypt)   |
| Frontend            | Jinja2, Bootstrap  |
| Testing             | Pytest             |
| Deployment          | Render             |

---

# 📁 Project Structure

```text
TodoApp/
│
├── alembic/
├── routers/
│   ├── auth.py
│   ├── todos.py
│   ├── users.py
│   └── admin.py
│
├── static/
│
├── templates/
│
├── tests/
│
├── database.py
├── models.py
├── main.py
├── requirements.txt
└── README.md
```

---

# 🏗 Architecture

```text
                Browser
                   │
                   ▼
         Jinja2 Templates
                   │
                   ▼
              FastAPI App
                   │
    ┌──────────────┼──────────────┐
    ▼              ▼              ▼
 Authentication   Todos        Admin
                   │
                   ▼
           SQLAlchemy ORM
                   │
                   ▼
            PostgreSQL / SQLite
```

---

# 🔐 Authentication Flow

```text
User Login
     │
     ▼
Credential Verification
     │
     ▼
JWT Token Generated
     │
     ▼
Token Stored in Browser Cookie
     │
     ▼
Protected Requests
     │
     ▼
Current User Retrieved
     │
     ▼
Authorized Endpoint Access
```

---

# 🗄 Database Schema

## Users

| Field           | Description        |
| --------------- | ------------------ |
| id              | Primary Key        |
| username        | Unique Username    |
| email           | User Email         |
| hashed_password | Encrypted Password |
| role            | User / Admin       |
| phone_number    | Contact Number     |
| is_active       | Active Status      |

---

## Todos

| Field       | Description            |
| ----------- | ---------------------- |
| id          | Primary Key            |
| title       | Todo Title             |
| description | Todo Description       |
| priority    | Task Priority          |
| complete    | Completion Status      |
| owner       | Foreign Key → Users.id |

---

# 📌 API Modules

## `auth.py`

Responsible for:

* User Registration
* Login
* JWT Generation
* Password Hashing
* Current User Authentication

---

## `todos.py`

Responsible for:

* Create Todo
* Read Todo
* Update Todo
* Delete Todo

Each authenticated user can only manage their own todos.

---

## `users.py`

Responsible for:

* View User Information
* Change Password
* Update Phone Number

---

## `admin.py`

Responsible for:

* View All Todos
* Delete Any Todo

Accessible only to Admin users.

---

# 🧪 Testing

The application includes unit tests using **Pytest**.

Coverage includes:

* Authentication
* Todo APIs
* User APIs
* Admin APIs
* Database Dependency Overrides

---

# 🗃 Database Migrations

Database schema changes are managed using **Alembic**.

Current migration includes:

* User phone number column
* Schema versioning
* Upgrade and downgrade support

---

# 🌐 Deployment

The application is deployed using:

* Render Web Service
* Render PostgreSQL Database

Deployment configuration includes:

* Environment Variables
* PostgreSQL Connection
* Production FastAPI Server

---

# 🚀 Local Development

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project:

```bash
cd 02_fastapi/TodoApp
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

API Documentation:

```text
http://127.0.0.1:8000/docs
```

---

# 📚 Learning Outcomes

Through this project, I gained hands-on experience with:

* FastAPI
* REST API Design
* SQLAlchemy ORM
* Alembic
* JWT Authentication
* OAuth2
* Dependency Injection
* Database Relationships
* PostgreSQL
* Pytest
* Cloud Deployment
* Backend Project Organization

---

# 🔮 Future Enhancements

Planned improvements include:

* Refresh Tokens
* Email Verification
* Password Reset
* Docker Support
* GitHub Actions CI/CD
* API Rate Limiting
* Structured Logging
* User Profile Images
* Responsive UI Redesign
* Dark Mode

---

# 👩‍💻 Author

**Saloni Azad**

Backend Engineer | Python | FastAPI | SQLAlchemy

Currently focused on building production-ready backend systems while preparing for Backend and AI Backend Engineering roles.
