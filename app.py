from flask import Flask, request, send_file, render_template
import yt_dlp
import uuid

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    link = request.json.get('link')
    platform = request.json.get('platform')

    # Generate a unique ID to avoid conflicts
    temp_dir = "/tmp"
    unique_id = str(uuid.uuid4())
    output_template = f"{temp_dir}/{unique_id}_%(title)s_{platform}_%(id)s.%(ext)s"

    ydl_opts = {
        'outtmpl': output_template,  # Use dynamic naming
        'quiet': True,
        'format': 'bestvideo+bestaudio/best',  # Download best quality available
    }

    try:
        # Download video using yt-dlp
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)

        # Find the downloaded file
        downloaded_file = next(
            (os.path.join(temp_dir, f) for f in os.listdir(temp_dir) if unique_id in f),
            None
        )

        if not downloaded_file:
            return {"error": "Failed to locate the downloaded file"}, 400

        # Send the file to the user
        return send_file(downloaded_file, as_attachment=True)

    except Exception as e:
        return {"error": str(e)}, 400
