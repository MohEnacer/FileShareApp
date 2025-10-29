# discovery.py
# broadcaster + listener to discover devices using UDP broadcast.

import socket
import time
import threading
from datetime import datetime
from config import DISCOVERY_PORT, BROADCAST_INTERVAL, HTTP_PORT
from utils import get_local_ip
import os

LOCAL_IP = get_local_ip()
HOSTNAME = socket.gethostname()

devices = {}  # key: ip|name -> {name, ip, port, last_seen}
devices_lock = threading.Lock()

def _make_message():
    return f"FILESHARE|{HOSTNAME}|{LOCAL_IP}|{HTTP_PORT}"

def discovery_broadcaster(stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = _make_message().encode("utf-8")
    while not stop_event.is_set():
        try:
            sock.sendto(msg, ("<broadcast>", DISCOVERY_PORT))
        except Exception:
            pass
        stop_event.wait(BROADCAST_INTERVAL)
    sock.close()

def discovery_listener(stop_event):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        sock.bind(("", DISCOVERY_PORT))
    except Exception:
        return
    sock.settimeout(1.0)
    while not stop_event.is_set():
        try:
            data, addr = sock.recvfrom(1024)
            text = data.decode("utf-8", errors="ignore")
            if text.startswith("FILESHARE|"):
                parts = text.split("|")
                if len(parts) >= 4:
                    _, name, ip, port = parts[:4]
                    if ip == LOCAL_IP:
                        continue
                    key = f"{ip}|{name}"
                    with devices_lock:
                        devices[key] = {"name": name, "ip": ip, "port": port, "last_seen": datetime.utcnow()}
        except socket.timeout:
            pass
        except Exception:
            pass
        # cleanup stale
        with devices_lock:
            remove = []
            for k, v in list(devices.items()):
                age = (datetime.utcnow() - v["last_seen"]).total_seconds()
                if age > (BROADCAST_INTERVAL * 6):
                    remove.append(k)
            for k in remove:
                devices.pop(k, None)
    sock.close()

def start_discovery_threads():
    stop_event = threading.Event()
    t1 = threading.Thread(target=discovery_broadcaster, args=(stop_event,), daemon=True)
    t2 = threading.Thread(target=discovery_listener, args=(stop_event,), daemon=True)
    t1.start(); t2.start()
    return stop_event  # caller can set() to stop threads
