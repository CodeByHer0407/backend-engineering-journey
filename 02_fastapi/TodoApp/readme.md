# 🚀 TodoApp - FastAPI Backend Application

## Overview

TodoApp is a backend REST API built using FastAPI, SQLAlchemy ORM, SQLite, and JWT Authentication.

The project demonstrates:

- User Registration
- User Authentication
- JWT Token Authorization
- CRUD Operations
- Role-Based Access Control (RBAC)
- Database Integration using SQLAlchemy ORM

This project is being built as part of my FastAPI learning journey while strengthening my backend engineering skills.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI | API Framework |
| SQLAlchemy | ORM |
| SQLite | Database |
| Pydantic | Request Validation |
| JWT | Authentication |
| Passlib (bcrypt) | Password Hashing |
| Uvicorn | ASGI Server |

---

## Project Architecture

```text
Client
  │
  ▼
FastAPI Routers
  │
  ├── auth.py
  ├── todos.py
  ├── users.py
  └── admin.py
  │
  ▼
SQLAlchemy ORM
  │
  ▼
SQLite Database
```

---

## Authentication Flow

### User Registration

```text
User Registration Request
          ↓
CreateUserRequest Validation
          ↓
Password Hashing (bcrypt)
          ↓
User Saved in Database
```

### User Login

```text
Username + Password
          ↓
Credential Verification
          ↓
JWT Token Generation
          ↓
Token Returned to User
```

### Authorized Requests

```text
Client Request
       ↓
JWT Token
       ↓
get_current_user()
       ↓
User Identified
       ↓
Protected Endpoint Access
```

---

## Database Schema

### Users Table

| Column | Description |
|----------|------------|
| id | Primary Key |
| username | Unique Username |
| email | User Email |
| hashed_password | Secure Password Hash |
| role | User/Admin |
| phone_number | Contact Number |

### Todos Table

| Column | Description |
|----------|------------|
| id | Primary Key |
| title | Todo Title |
| description | Todo Description |
| priority | Task Priority |
| complete | Completion Status |
| owner | Foreign Key → Users.id |

---

## API Modules

### auth.py

Responsible for:

- User Registration
- Login
- Password Hashing
- JWT Token Generation
- Current User Identification

### todos.py

Responsible for:

- Create Todo
- Read Todo
- Update Todo
- Delete Todo

Users can only access their own todos.

### users.py

Responsible for:

- View User Profile
- Change Password
- Update Phone Number

### admin.py

Responsible for:

- View All Todos
- Delete Any Todo

Accessible only to users with Admin role.

---

## Current Features

- JWT Authentication
- Password Hashing
- CRUD Operations
- SQLAlchemy ORM
- Role-Based Authorization
- Dependency Injection
- Request Validation using Pydantic
- Foreign Key Relationships

---

## Testing (Upcoming Section)

Planned additions after completing the testing module:

- Unit Testing
- Integration Testing
- Pytest Fixtures
- Dependency Overrides
- Test Database Isolation
- Coverage Reporting

---

## Database Migrations (Upcoming Section)

Planned additions after completing Alembic:

- Schema Versioning
- Migration Scripts
- Upgrade/Downgrade Support
- Production-safe Database Changes

---

## Full Stack Integration (Upcoming Section)

Planned additions:

- Frontend Integration
- API Consumption
- End-to-End Flow Documentation
- Screenshots and Architecture Diagrams

---

## Deployment (Upcoming Section)

Planned additions:

- Docker
- Cloud Deployment
- CI/CD Pipeline
- Environment Configuration

---

## Learning Outcomes

While building this project, I learned:

- FastAPI Routing
- Dependency Injection
- JWT Authentication
- Password Hashing
- SQLAlchemy ORM
- CRUD API Design
- Database Relationships
- Role-Based Access Control

---

## Future Improvements

- Refresh Tokens
- PostgreSQL Integration
- Dockerization
- CI/CD Pipeline
- API Rate Limiting
- Enhanced Logging & Monitoring

---

## Author

**Saloni Azad**

Backend Engineer | Python | FastAPI | SQLAlchemy

Currently learning backend system design and scalable API development.
