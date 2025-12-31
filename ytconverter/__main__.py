import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

EPILOG = """
Upcoming:
  ytconverter <url> -mp3 -b 128, 192, ...
  ytconverter <url> -mp4 -r 720, 1080, 4K, ...
  ytconverter <url> -multi_<mp4/mp3>
  ytconverter <url> --playlist
"""

def main():
    parser = argparse.ArgumentParser(
        description="YTConverter - YouTube Downloader CLI Tool",
        epilog=EPILOG,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False)

    mutually_exclusive_group = parser.add_mutually_exclusive_group()

    mutually_exclusive_group.add_argument(
        "-S", "-s", action="store_true", help="Launch the interactive menu and the main script.")

    mutually_exclusive_group.add_argument(
        "-U", "--update",
        action="store_true",
        help="Update YTConverter to the latest version via pip.")

    mutually_exclusive_group.add_argument(
        "-v", "--version", action="store_true", help="Show the current installed version.")

    mutually_exclusive_group.add_argument(
        "-h", "--help", action="help", help="Show this help message.")

    mutually_exclusive_group.add_argument(
        "--api", action="store_true", help="Launch the FastAPI REST API server.")

    # API server options (only used with --api)
    parser.add_argument(
        "--host", default="0.0.0.0", help="API server host (default: 0.0.0.0)")
    
    parser.add_argument(
        "--port", type=int, default=8000, help="API server port (default: 8000)")

    args = parser.parse_args()

    if args.update:
        from ytconverter.utils.update import update_self
        update_self()
        return

    elif args.version:
        from ytconverter.config import load_local_version
        local_version, version_type = load_local_version()
        print(f"YTConverter version: {local_version}")
        return

    elif args.S:
        from ytconverter.cli.menu import main_loop
        main_loop()
        return

    elif args.api:
        import uvicorn
        from ytconverter.api.app import app
        print(f"Starting YTConverter API server on {args.host}:{args.port}")
        print(f"API Documentation: http://{args.host}:{args.port}/docs")
        print(f"Set YTCONVERTER_API_KEYS environment variable to enable authentication")
        uvicorn.run(app, host=args.host, port=args.port)
        return

    else:
        parser.print_help()
        return

if __name__ == "__main__":
    main()
