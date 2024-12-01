from flask import Flask, request, render_template, send_file
from pytubefix import YouTube
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    try:
        url = request.form["url"]
        if not url:
            return "URL is required", 400
  
        yt = YouTube(url)
        mp3_audio = yt.streams.filter(only_audio=True).first()
        file_stream = io.BytesIO()
        mp3_audio.stream_to_buffer(file_stream)
        file_stream.seek(0)

        
        return send_file(file_stream, as_attachment=True, download_name=f'{yt.title}.mp3')

    except Exception as e:
        return f"An error opccurred: {str(e)}", 500

if __name__ == '__main__':
    app.run()
