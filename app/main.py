import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv

from config.database import connect_db, close_db
from routes import staff, students, classrooms, exams, allocations

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown events for the FastAPI app."""
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="CIA Test Duty Allocation API",
    version="1.0.0",
    lifespan=lifespan,
)

# ── Middleware ────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── API Routes ───────────────────────────────────────────────
app.include_router(staff.router, prefix="/api/staff", tags=["Staff"])
app.include_router(students.router, prefix="/api/students", tags=["Students"])
app.include_router(classrooms.router, prefix="/api/classrooms", tags=["Classrooms"])
app.include_router(exams.router, prefix="/api/exams", tags=["Exams"])
app.include_router(allocations.router, prefix="/api/allocations", tags=["Allocations"])


# ── Health check ─────────────────────────────────────────────
@app.get("/", tags=["Health"])
async def health_check():
    return {
        "message": "CIA Test Duty Allocation API",
        "version": "1.0.0",
        "endpoints": {
            "staff": "/api/staff",
            "classrooms": "/api/classrooms",
            "students": "/api/students",
            "exams": "/api/exams",
            "allocations": "/api/allocations",
        },
    }


# ── Global exception handler ─────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"},
    )
