"""Pydantic models for API request/response schemas."""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class DownloadRequest(BaseModel):
    """Base download request model."""
    url: str = Field(..., description="YouTube video or playlist URL")
    output_path: Optional[str] = Field(None, description="Custom output directory path")


class SingleMP3Request(DownloadRequest):
    """Request model for single MP3 download."""
    format_id: Optional[str] = Field(None, description="Specific audio format ID or 'bestaudio'")


class SingleMP4Request(DownloadRequest):
    """Request model for single MP4 download."""
    format_id: Optional[str] = Field(None, description="Specific video format ID")


class PlaylistRequest(DownloadRequest):
    """Request model for playlist downloads."""
    download_subtitles: bool = Field(False, description="Whether to download subtitles")
    subtitle_lang: Optional[str] = Field(None, description="Subtitle language code (e.g., 'en')")
    auto_subtitles: bool = Field(True, description="Download auto-generated subtitles if manual not available")


class VideoInfoRequest(BaseModel):
    """Request model for video information."""
    url: str = Field(..., description="YouTube video or playlist URL")


class FormatInfo(BaseModel):
    """Format information model."""
    format_id: str
    ext: str
    resolution: Optional[str] = None
    filesize: Optional[int] = None
    filesize_approx: Optional[int] = None
    acodec: Optional[str] = None
    vcodec: Optional[str] = None
    abr: Optional[float] = None
    vbr: Optional[float] = None


class VideoInfo(BaseModel):
    """Video information response model."""
    title: str
    duration: Optional[int] = None
    uploader: Optional[str] = None
    upload_date: Optional[str] = None
    view_count: Optional[int] = None
    thumbnail: Optional[str] = None
    description: Optional[str] = None
    formats: List[FormatInfo] = []


class DownloadResponse(BaseModel):
    """Download response model."""
    success: bool
    message: str
    file_path: Optional[str] = None
    title: Optional[str] = None
    duration: Optional[int] = None


class PlaylistDownloadResponse(BaseModel):
    """Playlist download response model."""
    success: bool
    message: str
    playlist_title: Optional[str] = None
    folder_path: Optional[str] = None
    video_count: Optional[int] = None


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    version: str
