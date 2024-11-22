from flask import Flask, request, send_file
import yt_dlp
from flask import render_template

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    link = request.json.get('link')
    platform = request.json.get('platform')

    output_file = "downloaded_video.mp4"

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


