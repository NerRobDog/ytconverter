"""FastAPI application for YTConverter."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ytconverter.api.routes import router
from ytconverter.config import load_local_version

# Get allowed origins from environment or default to all
ALLOWED_ORIGINS = os.environ.get("YTCONVERTER_CORS_ORIGINS", "*")
if ALLOWED_ORIGINS == "*":
    origins = ["*"]
else:
    origins = [origin.strip() for origin in ALLOWED_ORIGINS.split(",")]

# Create FastAPI app
app = FastAPI(
    title="YTConverter API",
    description="REST API for YouTube video/audio downloading using yt-dlp",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint."""
    version, _ = load_local_version()
    return {
        "message": "YTConverter API",
        "version": version,
        "docs": "/docs",
        "health": "/api/v1/health",
    }
