from flask import Flask, request, jsonify, send_file

import yt_dlp
import os

app = Flask(__name__)

# ✅ System ke default Downloads folder ka path lene ka tareeqa
DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

# ✅ Download Video Route
@app.route('/download', methods=['POST'])
def download_video():
    data = request.json
    video_url = data.get("url")

    if not video_url:
        return jsonify({"message": "URL is required"}), 400

    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOADS_FOLDER, '%(title)s.%(ext)s'),  # Save in Downloads folder
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)

        return jsonify({"message": "Download completed!", "link": f"/file/{os.path.basename(filename)}"})

    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500

# ✅ Serve Downloaded File
@app.route('/file/<filename>')
def serve_file(filename):
    return send_file(os.path.join(DOWNLOADS_FOLDER, filename), as_attachment=True)

# ✅ Home Route: Serve index.html (ab template folder ka zaroorat nahi)
@app.route('/')
def index():
    return send_file("index.html")  # Directly serve file from root

if __name__ == '__main__':
    app.run(debug=True)
