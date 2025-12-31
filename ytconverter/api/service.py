"""Download service wrapper for non-interactive programmatic access."""

import json
import subprocess as sp
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

import yt_dlp

from ytconverter.constants import URL_RE
from ytconverter.utils import sanitize

# Maximum length for sanitized titles
MAX_TITLE_LENGTH = 60


class DownloadService:
    """Service class for handling video/audio downloads programmatically."""
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate YouTube URL."""
        return bool(URL_RE.match(url))
    
    @staticmethod
    def _sanitize_title(title: str, max_length: int = MAX_TITLE_LENGTH) -> str:
        """
        Sanitize and truncate title for safe file naming.
        
        Args:
            title: Original title
            max_length: Maximum length for truncated title
            
        Returns:
            Sanitized and truncated title
        """
        return sanitize(title)[:max_length]
    
    @staticmethod
    def get_video_info(url: str) -> Dict[str, Any]:
        """
        Get video information without downloading.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary containing video information
            
        Raises:
            Exception: If unable to fetch video info
        """
        if not DownloadService.validate_url(url):
            raise ValueError("Invalid YouTube URL")
        
        ydl_opts = {
            "quiet": True,
            "no_warnings": True,
            "extract_flat": False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
        return {
            "title": info.get("title", "Unknown"),
            "duration": info.get("duration"),
            "uploader": info.get("uploader"),
            "upload_date": info.get("upload_date"),
            "view_count": info.get("view_count"),
            "thumbnail": info.get("thumbnail"),
            "description": info.get("description"),
            "formats": [
                {
                    "format_id": f.get("format_id"),
                    "ext": f.get("ext"),
                    "resolution": f.get("resolution"),
                    "filesize": f.get("filesize"),
                    "filesize_approx": f.get("filesize_approx"),
                    "acodec": f.get("acodec"),
                    "vcodec": f.get("vcodec"),
                    "abr": f.get("abr"),
                    "vbr": f.get("vbr"),
                }
                for f in info.get("formats", [])
            ]
        }
    
    @staticmethod
    def download_single_mp3(
        url: str,
        output_path: Optional[str] = None,
        format_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Download a single video as MP3.
        
        Args:
            url: YouTube video URL
            output_path: Custom output directory
            format_id: Specific audio format ID
            
        Returns:
            Dictionary with download result
        """
        if not DownloadService.validate_url(url):
            raise ValueError("Invalid YouTube URL")
        
        # Get video info
        info = DownloadService.get_video_info(url)
        title = DownloadService._sanitize_title(info["title"])
        
        # Determine output path
        if output_path:
            dest = Path(output_path)
        else:
            dest = Path.home() / "Downloads" / "audio"
        
        dest.mkdir(parents=True, exist_ok=True)
        
        # Determine format
        dl_format = format_id if format_id else "bestaudio/best"
        
        # Download
        output_template = str(dest / f"{title}.%(ext)s")
        start_time = time.time()
        
        cmd = [
            "yt-dlp",
            "-f", dl_format,
            "-x",
            "--audio-format", "mp3",
            "-o", output_template,
            url,
        ]
        
        result = sp.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Download failed: {result.stderr}")
        
        duration = int(time.time() - start_time)
        
        # Find the downloaded file using glob pattern
        downloaded_file = None
        mp3_files = list(dest.glob(f"{title}.mp3"))
        if mp3_files:
            downloaded_file = str(mp3_files[0])
        
        return {
            "success": True,
            "message": "MP3 downloaded successfully",
            "file_path": downloaded_file,
            "title": info["title"],
            "duration": duration,
        }
    
    @staticmethod
    def download_single_mp4(
        url: str,
        output_path: Optional[str] = None,
        format_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Download a single video as MP4.
        
        Args:
            url: YouTube video URL
            output_path: Custom output directory
            format_id: Specific video format ID
            
        Returns:
            Dictionary with download result
        """
        if not DownloadService.validate_url(url):
            raise ValueError("Invalid YouTube URL")
        
        # Get video info
        info = DownloadService.get_video_info(url)
        title = DownloadService._sanitize_title(info["title"])
        
        # Determine output path
        if output_path:
            dest = Path(output_path)
        else:
            dest = Path.home() / "Downloads" / "videos"
        
        dest.mkdir(parents=True, exist_ok=True)
        
        # Determine format (default to best video+audio)
        dl_format = format_id if format_id else "bestvideo+bestaudio/best"
        
        # Download
        output_file = dest / f"{title}.mp4"
        start_time = time.time()
        
        ydl_opts = {
            "format": dl_format,
            "outtmpl": str(output_file),
            "merge_output_format": "mp4",
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except yt_dlp.utils.DownloadError as e:
            raise RuntimeError(f"yt-dlp download failed: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error during download: {str(e)}")
        
        duration = int(time.time() - start_time)
        
        return {
            "success": True,
            "message": "MP4 downloaded successfully",
            "file_path": str(output_file),
            "title": info["title"],
            "duration": duration,
        }
    
    @staticmethod
    def _download_playlist_generic(
        url: str,
        format_type: str,
        output_path: Optional[str] = None,
        download_subtitles: bool = False,
        subtitle_lang: Optional[str] = None,
        auto_subtitles: bool = True
    ) -> Dict[str, Any]:
        """
        Generic playlist download helper for both MP3 and MP4.
        
        Args:
            url: YouTube playlist URL
            format_type: Either "mp3" or "mp4"
            output_path: Custom output directory
            download_subtitles: Whether to download subtitles
            subtitle_lang: Subtitle language code
            auto_subtitles: Download auto-generated subtitles
            
        Returns:
            Dictionary with download result
        """
        if not DownloadService.validate_url(url):
            raise ValueError("Invalid YouTube URL")
        
        # Get playlist info
        ydl_opts = {"quiet": True, "no_warnings": True, "extract_flat": True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        playlist_title = info.get("title") or info.get("playlist_title") or "playlist"
        safe_playlist_title = DownloadService._sanitize_title(playlist_title)
        
        # Determine output path
        if output_path:
            dest = Path(output_path)
        else:
            default_subdir = "audio" if format_type == "mp3" else "videos"
            dest = Path.home() / "Downloads" / default_subdir
        
        playlist_folder = dest / safe_playlist_title
        playlist_folder.mkdir(parents=True, exist_ok=True)
        
        # Build command
        output_template = str(playlist_folder / "%(playlist_index)03d - %(title)s.%(ext)s")
        cmd = ["yt-dlp", "-i", "--yes-playlist"]
        
        # Add format-specific options
        if format_type == "mp3":
            cmd.extend(["-x", "--audio-format", "mp3"])
        else:  # mp4
            cmd.extend(["-f", "bestvideo+bestaudio/best", "--merge-output-format", "mp4"])
        
        cmd.extend(["-o", output_template])
        
        # Add subtitle flags if requested
        if download_subtitles:
            cmd.append("--write-sub")
            if auto_subtitles:
                cmd.append("--write-auto-sub")
            if subtitle_lang:
                cmd.extend(["--sub-lang", subtitle_lang])
            cmd.extend(["--convert-subs", "srt"])
        
        cmd.append(url)
        
        # Download
        start_time = time.time()
        result = sp.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            raise RuntimeError(f"Playlist download failed: {result.stderr}")
        
        duration = int(time.time() - start_time)
        
        # Count downloaded files
        video_count = len(list(playlist_folder.glob(f"*.{format_type}")))
        
        return {
            "success": True,
            "message": "Playlist downloaded successfully",
            "playlist_title": playlist_title,
            "folder_path": str(playlist_folder),
            "video_count": video_count,
            "duration": duration,
        }
    
    @staticmethod
    def download_playlist_mp3(
        url: str,
        output_path: Optional[str] = None,
        download_subtitles: bool = False,
        subtitle_lang: Optional[str] = None,
        auto_subtitles: bool = True
    ) -> Dict[str, Any]:
        """
        Download a playlist as MP3 files.
        
        Args:
            url: YouTube playlist URL
            output_path: Custom output directory
            download_subtitles: Whether to download subtitles
            subtitle_lang: Subtitle language code
            auto_subtitles: Download auto-generated subtitles
            
        Returns:
            Dictionary with download result
        """
        return DownloadService._download_playlist_generic(
            url=url,
            format_type="mp3",
            output_path=output_path,
            download_subtitles=download_subtitles,
            subtitle_lang=subtitle_lang,
            auto_subtitles=auto_subtitles
        )
    
    @staticmethod
    def download_playlist_mp4(
        url: str,
        output_path: Optional[str] = None,
        download_subtitles: bool = False,
        subtitle_lang: Optional[str] = None,
        auto_subtitles: bool = True
    ) -> Dict[str, Any]:
        """
        Download a playlist as MP4 files.
        
        Args:
            url: YouTube playlist URL
            output_path: Custom output directory
            download_subtitles: Whether to download subtitles
            subtitle_lang: Subtitle language code
            auto_subtitles: Download auto-generated subtitles
            
        Returns:
            Dictionary with download result
        """
        return DownloadService._download_playlist_generic(
            url=url,
            format_type="mp4",
            output_path=output_path,
            download_subtitles=download_subtitles,
            subtitle_lang=subtitle_lang,
            auto_subtitles=auto_subtitles
        )
