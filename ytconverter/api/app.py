"""FastAPI application for YTConverter."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ytconverter.api.routes import router
from ytconverter.config import load_local_version

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
    allow_origins=["*"],  # Configure appropriately for production
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
