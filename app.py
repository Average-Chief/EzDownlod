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

    unique_id = uuid.uuid4().hex
    output_file = f"/tmp/downloaded_video_{unique_id}.mp4"

    ydl_opts = {
        'outtmpl': output_file,
        'quiet': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        return send_file(output_file, as_attachment=True)

    except Exception as e:
        return {"error": str(e)}, 400
