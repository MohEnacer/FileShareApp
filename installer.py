# installer.py
import shutil
from pathlib import Path
import sys
import os
from config import LOCALAPP, EXE_NAME, APP_NAME
from utils import get_executable_path

def create_desktop_bat(exe_target: Path):
    desktop = Path.home() / "Desktop"
    bat = desktop / f"{APP_NAME}_run.bat"
    if not bat.exists():
        bat.write_text(f'@echo off\nstart "" "{str(exe_target)}"\n', encoding="utf-8")

def install_or_update():
    """
    Copy current exe into LOCALAPP and create desktop shortcut .bat.
    Returns path to deployed exe in LOCALAPP.
    """
    LOCALAPP.mkdir(parents=True, exist_ok=True)
    current = get_executable_path()
    target_exe = LOCALAPP / EXE_NAME
    try:
        shutil.copy2(str(current), str(target_exe))
    except Exception as e:
        print("copy failed:", e)
    create_desktop_bat(target_exe)
    return target_exe

if __name__ == "__main__":
    print("Installing/updating...")
    print("Deployed to:", install_or_update())
