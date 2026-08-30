from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import students

# Create tables on startup if they don't already exist.
# (Existing tables/data are left untouched.)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Record Management API",
    description="A simple CRUD API for managing student records.",
    version="2.0.0",
)

# Allow the frontend to call the API during local development. Since the
# frontend is served by this same FastAPI app (see the static mount below),
# this is mainly a safety net for running the frontend separately
# (e.g. opening index.html directly or serving it with a different tool).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000",
        "http://127.0.0.1:5500",  # e.g. VS Code Live Server, if used instead
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(students.router)


@app.get("/api")
def home():
    return {"message": "Welcome to Student Record Management API"}


# Serve the frontend (index.html, style.css, script.js) at "/".
# Registered last so it doesn't shadow the API routes or /docs above.
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
