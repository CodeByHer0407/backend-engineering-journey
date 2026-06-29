# =============================================================================
# main.py
# Purpose : Application entry point. Creates the FastAPI instance, triggers
#           database table creation on startup, and registers all routers.
#           Run this file with: uvicorn main:app --reload
# =============================================================================


from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import models
from database import engine
from routers import admin, auth, todos, users

# Create the FastAPI application instance.
app = FastAPI(
    title="Todo Application",
    description="A full-stack Todo application built with FastAPI.",
    version="1.0.0",
)


# Create database tables if they don't already exist.
models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return RedirectResponse(
        url="/todos/todo-page",
        status_code=status.HTTP_302_FOUND
        )


@app.get("/health")
def health_checkup():
    return {"status": "healthy"}

# Register API routers.
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)