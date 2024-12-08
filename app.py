from flask import Flask, request, render_template, send_file
from audio_convert import convert_to_mp3
from tag_to_mp3 import tag_insert
from pytubefix import YouTube
import io
import os


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form.get("url")
        if not url:
            return "URL is required", 400
        
        yt = YouTube(url)
        
        convert_to_mp3(yt)
        tag_insert(yt)

        file_stream = io.BytesIO()
        mp3_file = f"{yt.title}.mp3"
        with open(mp3_file, "rb") as f:
            file_stream.write(f.read())
        file_stream.seek(0)
        os.remove(mp3_file)
        return send_file(file_stream, as_attachment=True, download_name=mp3_file)
    
    except Exception as e:
        return f"An error opccurred: {str(e)}", 500


if __name__ == '__main__':
    app.run()
