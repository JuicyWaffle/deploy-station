#!/usr/bin/env python3
"""Deploy Station — lightweight deploy server (stdlib only)."""

import cgi
import json
import os
import shutil
import subprocess
import tempfile
import zipfile
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime

PORT = 8080
PROJECTS_DIR = Path.home() / "projects"
PUBLIC_DIR = Path(__file__).resolve().parent.parent / "public"


class DeployHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self._serve_file(PUBLIC_DIR / "index.html", "text/html")
        elif self.path == "/api/projects":
            self._list_projects()
        elif self.path.startswith("/public/"):
            rel = self.path[len("/public/"):]
            self._serve_file(PUBLIC_DIR / rel)
        else:
            self._json_response(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/api/deploy":
            self._handle_deploy()
        else:
            self._json_response(404, {"error": "not found"})

    # --- API handlers ---

    def _list_projects(self):
        projects = []
        if PROJECTS_DIR.is_dir():
            for entry in sorted(PROJECTS_DIR.iterdir()):
                if entry.is_dir() and not entry.name.startswith("."):
                    # Skip deploy-station itself
                    if entry.name == "deploy-station":
                        continue
                    is_git = (entry / ".git").is_dir()
                    projects.append({"name": entry.name, "git": is_git})
        self._json_response(200, {"projects": projects})

    def _handle_deploy(self):
        try:
            content_type = self.headers.get("Content-Type", "")

            if "multipart/form-data" in content_type:
                form = cgi.FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={
                        "REQUEST_METHOD": "POST",
                        "CONTENT_TYPE": content_type,
                    },
                )
                project_name = form.getfirst("project", "")
                file_item = form["file"]
                if not hasattr(file_item, "file"):
                    self._json_response(400, {"error": "geen zip bestand ontvangen"})
                    return
                zip_data = file_item.file.read()
            else:
                self._json_response(400, {"error": "verwacht multipart/form-data"})
                return

            if not project_name:
                self._json_response(400, {"error": "geen project geselecteerd"})
                return

            # Validate project name (prevent path traversal)
            if "/" in project_name or "\\" in project_name or project_name.startswith("."):
                self._json_response(400, {"error": "ongeldige projectnaam"})
                return

            project_dir = PROJECTS_DIR / project_name
            if not project_dir.is_dir():
                self._json_response(400, {"error": f"project '{project_name}' bestaat niet"})
                return

            # Extract to temp dir
            tmp_dir = tempfile.mkdtemp(prefix="deploy-station-")
            try:
                tmp_zip = os.path.join(tmp_dir, "upload.zip")
                with open(tmp_zip, "wb") as f:
                    f.write(zip_data)

                if not zipfile.is_zipfile(tmp_zip):
                    self._json_response(400, {"error": "ongeldig zip bestand"})
                    return

                extract_dir = os.path.join(tmp_dir, "extracted")
                with zipfile.ZipFile(tmp_zip, "r") as zf:
                    # Security: check for path traversal in zip entries
                    for name in zf.namelist():
                        if name.startswith("/") or ".." in name:
                            self._json_response(400, {"error": f"onveilig pad in zip: {name}"})
                            return
                    zf.extractall(extract_dir)

                # Determine source: if zip has single root dir, use its contents
                entries = os.listdir(extract_dir)
                if len(entries) == 1 and os.path.isdir(os.path.join(extract_dir, entries[0])):
                    source_dir = os.path.join(extract_dir, entries[0])
                else:
                    source_dir = extract_dir

                # Copy files to project
                deployed_files = []
                for root, dirs, files in os.walk(source_dir):
                    # Skip hidden dirs
                    dirs[:] = [d for d in dirs if not d.startswith(".")]
                    for fname in files:
                        if fname.startswith("."):
                            continue
                        src = os.path.join(root, fname)
                        rel = os.path.relpath(src, source_dir)
                        dst = project_dir / rel
                        dst.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src, dst)
                        deployed_files.append(rel)

                # Git commit + push
                git_output = ""
                is_git = (project_dir / ".git").is_dir()
                if is_git:
                    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
                    msg = f"deploy: {timestamp} from claude ({len(deployed_files)} files)"
                    try:
                        result = subprocess.run(
                            ["git", "add", "-A"],
                            cwd=str(project_dir),
                            capture_output=True, text=True, timeout=30,
                        )
                        git_output += result.stdout + result.stderr

                        result = subprocess.run(
                            ["git", "commit", "-m", msg],
                            cwd=str(project_dir),
                            capture_output=True, text=True, timeout=30,
                        )
                        git_output += result.stdout + result.stderr

                        result = subprocess.run(
                            ["git", "push"],
                            cwd=str(project_dir),
                            capture_output=True, text=True, timeout=60,
                        )
                        git_output += result.stdout + result.stderr
                    except subprocess.TimeoutExpired:
                        git_output += "\n[timeout bij git operatie]"
                    except Exception as e:
                        git_output += f"\n[git fout: {e}]"

                self._json_response(200, {
                    "ok": True,
                    "project": project_name,
                    "files": deployed_files,
                    "count": len(deployed_files),
                    "git": is_git,
                    "git_output": git_output.strip(),
                })

            finally:
                shutil.rmtree(tmp_dir, ignore_errors=True)

        except Exception as e:
            self._json_response(500, {"error": str(e)})

    # --- Helpers ---

    def _serve_file(self, filepath, content_type=None):
        filepath = Path(filepath)
        if not filepath.is_file():
            self._json_response(404, {"error": "not found"})
            return
        if content_type is None:
            ext = filepath.suffix.lower()
            content_type = {
                ".html": "text/html",
                ".css": "text/css",
                ".js": "application/javascript",
                ".json": "application/json",
                ".png": "image/png",
                ".svg": "image/svg+xml",
            }.get(ext, "application/octet-stream")
        data = filepath.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def _json_response(self, status, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        print(f"[deploy-station] {args[0]}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), DeployHandler)
    print(f"Deploy Station draait op http://localhost:{PORT}")
    print(f"Projects dir: {PROJECTS_DIR}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer gestopt.")
        server.server_close()
