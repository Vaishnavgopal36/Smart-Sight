# backend/server/app/config.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes import router
from settings import STATIC_DIR  # Updated import

app = FastAPI()

def setup_cors():
    app.add_middleware(
        CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Default Vite port; adjust if different
        "http://127.0.0.1:5173",  # Alternative localhost format
        "http://localhost:3000",  # Common React port, if applicable
    ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router)
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

setup_cors()