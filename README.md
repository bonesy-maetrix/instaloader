# InstaFlaskAPI (Render-Ready)

## 📦 Overview
This is a hosted Flask API backend for the iOS Instagram profile downloader.

## 📡 Endpoints
- `POST /api/download` → Accepts list of usernames, returns ZIP link
- `GET /api/download_zip?path=...` → Returns zipped profile media

## 🚀 Deploy on Render.com
1. Push to a GitHub repo
2. Connect Render
3. Autodeploy with `render.yaml` config

## 🛠 Dependencies
- Flask
- Flask-CORS
- Instaloader

