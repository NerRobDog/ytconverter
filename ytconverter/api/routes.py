"""API routes for YTConverter."""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from ytconverter.api.models import (
    SingleMP3Request,
    SingleMP4Request,
    PlaylistRequest,
    VideoInfoRequest,
    DownloadResponse,
    PlaylistDownloadResponse,
    VideoInfo,
    ErrorResponse,
)
from ytconverter.api.auth import verify_api_key
from ytconverter.api.service import DownloadService

router = APIRouter(prefix="/api/v1", tags=["downloads"])


@router.get("/health")
async def health_check():
    """Health check endpoint."""
    from ytconverter.config import load_local_version
    version, _ = load_local_version()
    return {"status": "ok", "version": version}


@router.post("/info", response_model=VideoInfo)
async def get_video_info(
    request: VideoInfoRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Get video information without downloading.
    
    Requires X-API-Key header for authentication.
    """
    try:
        info = DownloadService.get_video_info(request.url)
        return VideoInfo(**info)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch video info: {str(e)}")


@router.post("/download/single-mp3", response_model=DownloadResponse)
async def download_single_mp3(
    request: SingleMP3Request,
    api_key: str = Depends(verify_api_key)
):
    """
    Download a single video as MP3.
    
    Requires X-API-Key header for authentication.
    """
    try:
        result = DownloadService.download_single_mp3(
            url=request.url,
            output_path=request.output_path,
            format_id=request.format_id
        )
        return DownloadResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.post("/download/single-mp4", response_model=DownloadResponse)
async def download_single_mp4(
    request: SingleMP4Request,
    api_key: str = Depends(verify_api_key)
):
    """
    Download a single video as MP4.
    
    Requires X-API-Key header for authentication.
    """
    try:
        result = DownloadService.download_single_mp4(
            url=request.url,
            output_path=request.output_path,
            format_id=request.format_id
        )
        return DownloadResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Download failed: {str(e)}")


@router.post("/download/playlist-mp3", response_model=PlaylistDownloadResponse)
async def download_playlist_mp3(
    request: PlaylistRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Download a playlist as MP3 files.
    
    Requires X-API-Key header for authentication.
    """
    try:
        result = DownloadService.download_playlist_mp3(
            url=request.url,
            output_path=request.output_path,
            download_subtitles=request.download_subtitles,
            subtitle_lang=request.subtitle_lang,
            auto_subtitles=request.auto_subtitles
        )
        return PlaylistDownloadResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playlist download failed: {str(e)}")


@router.post("/download/playlist-mp4", response_model=PlaylistDownloadResponse)
async def download_playlist_mp4(
    request: PlaylistRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Download a playlist as MP4 files.
    
    Requires X-API-Key header for authentication.
    """
    try:
        result = DownloadService.download_playlist_mp4(
            url=request.url,
            output_path=request.output_path,
            download_subtitles=request.download_subtitles,
            subtitle_lang=request.subtitle_lang,
            auto_subtitles=request.auto_subtitles
        )
        return PlaylistDownloadResponse(**result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Playlist download failed: {str(e)}")
