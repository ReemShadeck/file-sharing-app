from flask import Flask, request, send_from_directory, jsonify
import os
import time
import json
import uuid
from threading import Thread

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
METADATA_FILE = "metadata.json"
EXPIRATION_TIME = 86400  # 24 hours

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Ensure metadata file exists
if not os.path.exists(METADATA_FILE):
    with open(METADATA_FILE, "w") as f:
        json.dump({}, f)

# Background cleanup thread
def cleanup_files():
    while True:
        time.sleep(600)
        with open(METADATA_FILE, "r+") as f:
            metadata = json.load(f)
            for file, data in list(metadata.items()):
                filepath = os.path.join(UPLOAD_FOLDER, file)
                if os.path.isfile(filepath) and data.get('expires', True) and time.time() - data.get('timestamp', 0) > EXPIRATION_TIME:
                    try:
                        os.remove(filepath)
                        del metadata[file]
                    except Exception as e:
                        print(f"Error deleting {file}: {e}")
            f.seek(0)
            f.truncate()
            json.dump(metadata, f)

Thread(target=cleanup_files, daemon=True).start()

@app.route("/upload", methods=["POST"])
def upload_file():
    files = request.files.getlist("file")
    notes = request.form.get("notes", "")
    expires = request.form.get("expires") == "true"
    timestamp = time.time()
    uploaded_files = []

    with open(METADATA_FILE, "r+") as f:
        metadata = json.load(f)
        for file in files:
            if file and file.filename:
                safe_filename = file.filename.replace(' ', '_')
                file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
                file.save(file_path)
                metadata[safe_filename] = {
                    "timestamp": timestamp,
                    "note": notes,
                    "expires": expires
                }
                uploaded_files.append({"name": safe_filename, "url": f"/files/{safe_filename}"})
        f.seek(0)
        f.truncate()
        json.dump(metadata, f)

    return jsonify({"message": "Upload successful", "files": uploaded_files})

@app.route("/files/<filename>")
def get_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

@app.route("/files", methods=["GET"])
def list_files():
    with open(METADATA_FILE, "r") as f:
        metadata = json.load(f)
    return jsonify(metadata)

@app.route("/delete/<filename>", methods=["POST"])
def delete_file(filename):
    with open(METADATA_FILE, "r+") as f:
        metadata = json.load(f)
        if filename in metadata:
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
            del metadata[filename]
            f.seek(0)
            f.truncate()
            json.dump(metadata, f)
    return jsonify({"message": "File deleted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)