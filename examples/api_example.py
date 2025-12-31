#!/usr/bin/env python3
"""
Example script demonstrating YTConverter API usage.

This script shows how to interact with the YTConverter API programmatically.
"""

import requests
import json

# API Configuration
API_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key-here"  # Set to None if running in open mode

# Headers
headers = {
    "Content-Type": "application/json"
}

if API_KEY:
    headers["X-API-Key"] = API_KEY


def test_health():
    """Test API health endpoint."""
    print("Testing health endpoint...")
    response = requests.get(f"{API_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_video_info(url):
    """Test video info endpoint."""
    print(f"Testing video info for: {url}")
    response = requests.post(
        f"{API_URL}/info",
        headers=headers,
        json={"url": url}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Title: {data['title']}")
        print(f"Duration: {data.get('duration', 'N/A')} seconds")
        print(f"Uploader: {data.get('uploader', 'N/A')}")
        print(f"Formats available: {len(data.get('formats', []))}")
    else:
        print(f"Error: {response.json()}")
    print()


def test_download_mp3(url, output_path=None):
    """Test MP3 download endpoint."""
    print(f"Testing MP3 download for: {url}")
    payload = {"url": url}
    if output_path:
        payload["output_path"] = output_path
    
    response = requests.post(
        f"{API_URL}/download/single-mp3",
        headers=headers,
        json=payload
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Message: {data['message']}")
        print(f"File path: {data.get('file_path', 'N/A')}")
        print(f"Title: {data.get('title', 'N/A')}")
    else:
        print(f"Error: {response.json()}")
    print()


def test_download_mp4(url, output_path=None):
    """Test MP4 download endpoint."""
    print(f"Testing MP4 download for: {url}")
    payload = {"url": url}
    if output_path:
        payload["output_path"] = output_path
    
    response = requests.post(
        f"{API_URL}/download/single-mp4",
        headers=headers,
        json=payload
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Message: {data['message']}")
        print(f"File path: {data.get('file_path', 'N/A')}")
        print(f"Title: {data.get('title', 'N/A')}")
    else:
        print(f"Error: {response.json()}")
    print()


def test_playlist_mp3(url, output_path=None):
    """Test playlist MP3 download endpoint."""
    print(f"Testing playlist MP3 download for: {url}")
    payload = {
        "url": url,
        "download_subtitles": False,
        "auto_subtitles": True
    }
    if output_path:
        payload["output_path"] = output_path
    
    response = requests.post(
        f"{API_URL}/download/playlist-mp3",
        headers=headers,
        json=payload
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data['success']}")
        print(f"Message: {data['message']}")
        print(f"Playlist title: {data.get('playlist_title', 'N/A')}")
        print(f"Folder path: {data.get('folder_path', 'N/A')}")
        print(f"Video count: {data.get('video_count', 'N/A')}")
    else:
        print(f"Error: {response.json()}")
    print()


if __name__ == "__main__":
    # Test health endpoint (no auth required)
    test_health()
    
    # Example YouTube video URL (replace with actual URL when testing)
    # test_video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    # Uncomment to test with real URLs:
    # test_video_info(test_video_url)
    # test_download_mp3(test_video_url, "/tmp/downloads")
    # test_download_mp4(test_video_url, "/tmp/downloads")
    
    # Example playlist URL (replace with actual URL when testing)
    # test_playlist_url = "https://www.youtube.com/playlist?list=..."
    # test_playlist_mp3(test_playlist_url, "/tmp/downloads")
    
    print("All tests completed!")
    print("\nNote: Uncomment test functions with real URLs to test actual downloads.")
