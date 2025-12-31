# YTConverter REST API Documentation

YTConverter now includes a REST API backend powered by FastAPI, allowing you to integrate YouTube downloading functionality into your applications, bots, and services.

## Quick Start

### Installation

Install YTConverter with API dependencies:

```bash
pip install -r requirements.txt
```

### Starting the API Server

Launch the API server:

```bash
ytconverter --api
```

By default, the API runs on `http://0.0.0.0:8000`. You can customize the host and port:

```bash
ytconverter --api --host 127.0.0.1 --port 5000
```

### API Documentation

Once the server is running, access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Authentication

The API supports API key authentication via the `X-API-Key` header.

### Configuration

Set valid API keys using the `YTCONVERTER_API_KEYS` environment variable:

```bash
export YTCONVERTER_API_KEYS="key1,key2,key3"
ytconverter --api
```

If no API keys are configured, the API runs in **open mode** (no authentication required).

### Usage

Include the `X-API-Key` header in your requests:

```bash
curl -H "X-API-Key: your-api-key-here" http://localhost:8000/api/v1/health
```

## API Endpoints

### Health Check

**GET** `/api/v1/health`

Check API health and version.

**Response:**
```json
{
  "status": "ok",
  "version": "4.0.2.1"
}
```

### Get Video Information

**POST** `/api/v1/info`

Fetch video metadata without downloading.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
}
```

**Response:**
```json
{
  "title": "Video Title",
  "duration": 212,
  "uploader": "Channel Name",
  "upload_date": "20230101",
  "view_count": 1000000,
  "thumbnail": "https://...",
  "description": "Video description...",
  "formats": [
    {
      "format_id": "137",
      "ext": "mp4",
      "resolution": "1920x1080",
      "filesize": 50000000,
      "vcodec": "avc1.640028",
      "acodec": "none"
    }
  ]
}
```

### Download Single MP3

**POST** `/api/v1/download/single-mp3`

Download a single video as MP3.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "output_path": "/path/to/output",
  "format_id": "bestaudio"
}
```

**Response:**
```json
{
  "success": true,
  "message": "MP3 downloaded successfully",
  "file_path": "/path/to/output/Video_Title.mp3",
  "title": "Video Title",
  "duration": 15
}
```

### Download Single MP4

**POST** `/api/v1/download/single-mp4`

Download a single video as MP4.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "output_path": "/path/to/output",
  "format_id": "137+140"
}
```

**Response:**
```json
{
  "success": true,
  "message": "MP4 downloaded successfully",
  "file_path": "/path/to/output/Video_Title.mp4",
  "title": "Video Title",
  "duration": 25
}
```

### Download Playlist as MP3

**POST** `/api/v1/download/playlist-mp3`

Download all videos in a playlist as MP3 files.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/playlist?list=...",
  "output_path": "/path/to/output",
  "download_subtitles": false,
  "subtitle_lang": "en",
  "auto_subtitles": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Playlist downloaded successfully",
  "playlist_title": "My Playlist",
  "folder_path": "/path/to/output/My_Playlist",
  "video_count": 15,
  "duration": 180
}
```

### Download Playlist as MP4

**POST** `/api/v1/download/playlist-mp4`

Download all videos in a playlist as MP4 files.

**Request Body:**
```json
{
  "url": "https://www.youtube.com/playlist?list=...",
  "output_path": "/path/to/output",
  "download_subtitles": true,
  "subtitle_lang": "en",
  "auto_subtitles": true
}
```

**Response:**
```json
{
  "success": true,
  "message": "Playlist downloaded successfully",
  "playlist_title": "My Playlist",
  "folder_path": "/path/to/output/My_Playlist",
  "video_count": 15,
  "duration": 240
}
```

## Usage Examples

### cURL

#### Get Video Info
```bash
curl -X POST http://localhost:8000/api/v1/info \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}'
```

#### Download MP3
```bash
curl -X POST http://localhost:8000/api/v1/download/single-mp3 \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "output_path": "/tmp/downloads"}'
```

### Python Requests

```python
import requests

API_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key"

headers = {
    "X-API-Key": API_KEY,
    "Content-Type": "application/json"
}

# Get video info
response = requests.post(
    f"{API_URL}/info",
    headers=headers,
    json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
)
info = response.json()
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']} seconds")

# Download MP3
response = requests.post(
    f"{API_URL}/download/single-mp3",
    headers=headers,
    json={
        "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "output_path": "/tmp/downloads"
    }
)
result = response.json()
print(f"Downloaded: {result['file_path']}")
```

### Telegram Bot Integration

```python
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

API_URL = "http://localhost:8000/api/v1"
API_KEY = "your-api-key"

def download_audio(update: Update, context: CallbackContext):
    """Download audio from YouTube URL."""
    url = context.args[0] if context.args else None
    
    if not url:
        update.message.reply_text("Please provide a YouTube URL")
        return
    
    update.message.reply_text("Downloading audio...")
    
    try:
        response = requests.post(
            f"{API_URL}/download/single-mp3",
            headers={"X-API-Key": API_KEY},
            json={"url": url}
        )
        
        if response.status_code == 200:
            result = response.json()
            update.message.reply_text(f"✅ Downloaded: {result['title']}")
            # You can send the file back to the user here
        else:
            update.message.reply_text(f"❌ Error: {response.json()['detail']}")
    except Exception as e:
        update.message.reply_text(f"❌ Error: {str(e)}")

def main():
    updater = Updater("YOUR_TELEGRAM_BOT_TOKEN")
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("download", download_audio))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
```

### JavaScript/Node.js (axios)

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:8000/api/v1';
const API_KEY = 'your-api-key';

const headers = {
    'X-API-Key': API_KEY,
    'Content-Type': 'application/json'
};

// Get video info
async function getVideoInfo(url) {
    const response = await axios.post(
        `${API_URL}/info`,
        { url },
        { headers }
    );
    return response.data;
}

// Download MP3
async function downloadMP3(url, outputPath) {
    const response = await axios.post(
        `${API_URL}/download/single-mp3`,
        { url, output_path: outputPath },
        { headers }
    );
    return response.data;
}

// Example usage
(async () => {
    const url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ';
    
    const info = await getVideoInfo(url);
    console.log(`Title: ${info.title}`);
    
    const result = await downloadMP3(url, '/tmp/downloads');
    console.log(`Downloaded: ${result.file_path}`);
})();
```

## Configuration

### Storage Paths

By default, files are downloaded to:
- **Audio (MP3)**: `~/Downloads/audio/`
- **Video (MP4)**: `~/Downloads/videos/`

You can override these paths in each API request using the `output_path` parameter.

### Environment Variables

- `YTCONVERTER_API_KEYS`: Comma-separated list of valid API keys
  - Example: `export YTCONVERTER_API_KEYS="key1,key2,key3"`
  - If not set, the API runs in open mode (no authentication)

- `YTCONVERTER_CORS_ORIGINS`: CORS allowed origins (comma-separated or "*" for all)
  - Production: `export YTCONVERTER_CORS_ORIGINS="https://yourdomain.com,https://api.yourdomain.com"`
  - Development: `export YTCONVERTER_CORS_ORIGINS="*"` (default)
  - Security: Always restrict CORS origins in production

## Docker Deployment

### Basic Docker Setup

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose API port
EXPOSE 8000

# Run API server
CMD ["python", "-m", "ytconverter", "--api", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t ytconverter-api .
docker run -p 8000:8000 -e YTCONVERTER_API_KEYS="your-api-key" ytconverter-api
```

### Docker Compose with Redis

For advanced deployments with Redis caching:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - YTCONVERTER_API_KEYS=your-api-key
      - REDIS_URL=redis://redis:6379
    volumes:
      - ./downloads:/downloads
    depends_on:
      - redis
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## Rate Limiting

Rate limiting should be implemented at the infrastructure level:

- **Docker/Nginx**: Use nginx rate limiting
- **Redis**: Implement token bucket with Redis
- **Cloud**: Use API Gateway rate limiting (AWS API Gateway, Google Cloud Endpoints)

## Error Handling

The API returns standard HTTP status codes:

- `200`: Success
- `400`: Bad Request (invalid URL, missing parameters)
- `401`: Unauthorized (missing API key)
- `403`: Forbidden (invalid API key)
- `500`: Internal Server Error (download failed, service error)

Error responses follow this format:

```json
{
  "detail": "Error message describing what went wrong"
}
```

## Best Practices

1. **API Keys**: Always use API keys in production
2. **Rate Limiting**: Implement rate limiting at infrastructure level
3. **Storage**: Use persistent volumes for Docker deployments
4. **Monitoring**: Monitor API health endpoint for service status
5. **Caching**: Consider implementing Redis caching for popular videos
6. **Logging**: Enable application logging for debugging

## Support

For issues and questions:
- GitHub: https://github.com/kaifcodec/ytconverter
- Documentation: Check `/docs` endpoint when server is running

## License

See LICENSE file in the repository.
