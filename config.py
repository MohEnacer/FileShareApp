# config.py
APP_NAME = "FileShareApp"
APP_VERSION = "1.0.0"

HTTP_PORT = 8000
DISCOVERY_PORT = 5001
BROADCAST_INTERVAL = 4  # seconds

from pathlib import Path
import os

USER_DOCS = Path(os.path.expanduser("~")) / "Documents"
SHARED_FOLDER = USER_DOCS / "Partage"

from pathlib import Path
LOCALAPP = Path(os.getenv("LOCALAPPDATA", str(Path.home()))) / APP_NAME
EXE_NAME = "FileShareApp.exe"  # name to copy into LOCALAPP
