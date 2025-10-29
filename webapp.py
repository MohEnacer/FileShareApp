# webapp.py
from flask import Flask, request, send_from_directory, render_template, jsonify, render_template_string
from config import SHARED_FOLDER, HTTP_PORT
from pathlib import Path
from discovery import devices, devices_lock
from utils import ensure_folder, get_local_ip
import os

ensure_folder(SHARED_FOLDER)

app = Flask(__name__, template_folder="templates")

# index uses external template file templates/index.html
@app.route("/", methods=["GET"])
def index():
    files = sorted([f for f in os.listdir(SHARED_FOLDER)])
    with devices_lock:
        devs = [{"name": v["name"], "ip": v["ip"], "port": v["port"]} for v in devices.values()]
    return render_template("index.html", files=files, devices=devs, local_ip=get_local_ip(), port=HTTP_PORT)

@app.route("/files/<path:filename>")
def files_route(filename):
    return send_from_directory(str(SHARED_FOLDER), filename, as_attachment=True)

@app.route("/receive", methods=["POST"])
def receive():
    f = request.files.get("file")
    if not f:
        return ("no file sent", 400)
    safe_name = os.path.basename(f.filename)
    dest = Path(SHARED_FOLDER) / safe_name
    f.save(str(dest))
    # try remove Zone.Identifier if any (best-effort)
    try:
        zid = str(dest) + ":Zone.Identifier"
        if os.path.exists(zid):
            os.remove(zid)
    except Exception:
        pass
    return (f"received {safe_name}", 200)

@app.route("/devices")
def devices_api():
    with devices_lock:
        return jsonify([{"name": v["name"], "ip": v["ip"], "port": v["port"]} for v in devices.values()])
