# utils.py
import socket
import os
from pathlib import Path
import sys

def get_local_ip():
    """Return local LAN IP (best-effort)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def ensure_folder(path):
    Path(path).mkdir(parents=True, exist_ok=True)

def is_frozen():
    """Return True when running as bundled exe by PyInstaller."""
    return getattr(sys, "frozen", False)

def get_executable_path():
    """Return running executable path (if frozen) or script path."""
    if is_frozen():
        return Path(sys.executable)
    else:
        return Path(__file__).resolve().parent / "run.py"  # when running from source use run.py
