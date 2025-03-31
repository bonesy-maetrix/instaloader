from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import instaloader
import os
import shutil
import zipfile
from datetime import datetime

app = Flask(__name__)
CORS(app)

DOWNLOAD_ROOT = "downloads"

@app.route("/api/download", methods=["POST"])
def download_profiles():
    data = request.json
    usernames = data.get("usernames", [])
    tag = data.get("tag", "session")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    session_dir = os.path.join(DOWNLOAD_ROOT, f"{tag}_{timestamp}")
    os.makedirs(session_dir, exist_ok=True)

    try:
        for username in usernames:
            L = instaloader.Instaloader()
            profile_dir = os.path.join(session_dir, username)
            os.makedirs(profile_dir, exist_ok=True)
            profile = instaloader.Profile.from_username(L.context, username)

            count = 0
            for post in profile.get_posts():
                L.download_post(post, target=profile_dir)
                count += 1
                for file in os.listdir(profile_dir):
                    if file.startswith(post.shortcode) and not file.endswith(".txt"):
                        ext = os.path.splitext(file)[1]
                        new_name = f"{username}({count}){ext}"
                        os.rename(os.path.join(profile_dir, file), os.path.join(profile_dir, new_name))

        zip_path = os.path.join(DOWNLOAD_ROOT, f"{tag}_{timestamp}.zip")
        shutil.make_archive(zip_path.replace(".zip", ""), 'zip', session_dir)

        return jsonify({ "download_url": f"/api/download_zip?path={zip_path}" })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500

@app.route("/api/download_zip")
def get_zip():
    path = request.args.get("path")
    return send_file(path, as_attachment=True)
