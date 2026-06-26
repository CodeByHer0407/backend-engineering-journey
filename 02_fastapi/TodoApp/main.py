# =============================================================================
# main.py
# Purpose : Application entry point. Creates the FastAPI instance, triggers
#           database table creation on startup, and registers all routers.
#           Run this file with: uvicorn main:app --reload
# =============================================================================


from fastapi import FastAPI, Request, status
import models
from database import engine
from routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Create the FastAPI application instance.
app = FastAPI()


# On startup, create all tables defined in models.py if they don't already exist.
# This is safe to run every time — SQLAlchemy skips tables that already exist.
# 'bind=engine' tells SQLAlchemy which database connection to use.
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def test(request: Request):
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)




@app.get("/healthy")
def health_checkup():
    return {'status': 'Healthy'}

# Register routers — each handles a logical group of API endpoints:
#   auth  → /auth/...   (login, register, JWT token generation)
#   todos → /todos/...  (CRUD operations for todo items)
#   admin → /admin/...  (admin-only operations, e.g. view all users/todos)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)