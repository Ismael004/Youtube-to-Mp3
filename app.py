from flask import Flask, request, render_template, send_file
from pytubefix import YouTube
from pydub import AudioSegment
import io
import os
import eyed3
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Função para baixar e converter a thumbnail para JPEG
def download_and_convert_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url, stream=True)
    print(f"Thumbnail URL: {thumbnail_url}")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        # Converte a imagem para JPEG
        image = Image.open(BytesIO(response.content))
        # Converte para RGB caso seja necessário
        converted_image = BytesIO()
        image.convert("RGB").save(converted_image, format="JPEG")
        converted_image.seek(0)
        print(f"Converted thumbnail size: {len(converted_image.getvalue())} bytes")
        return converted_image.read()
    return None

@app.route('/download', methods=['POST'])
def download():
    try:
        # Obtém a URL do vídeo
        url = request.form.get("url")
        if not url:
            return "URL is required", 400

        # Converte para MP3
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if not audio_stream:
            return "No audio stream found", 400

        # Baixa o áudio
        downloaded_file = audio_stream.download(filename=f"{yt.title}.mp4")
        
        # Converte para MP3
        audio = AudioSegment.from_file(downloaded_file)
        mp3_filename = f"{yt.title}.mp3"
        audio.export(mp3_filename, format="mp3")
        os.remove(downloaded_file)  # Remove o arquivo original (MP4 ou M4A)

        # Obtém e converte a miniatura
        thumbnail_url = yt.thumbnail_url
        thumbnail_data = download_and_convert_thumbnail(thumbnail_url)
        if thumbnail_data is None:
            return "Failed to download or convert the thumbnail", 500

        # Adiciona tags ID3 ao arquivo MP3
        audiofile = eyed3.load(mp3_filename)
        if audiofile.tag is None:
            audiofile.initTag()
        audiofile.tag.artist = yt.author
        audiofile.tag.title = yt.title
        audiofile.tag.images.set(
            eyed3.id3.frames.ImageFrame.FRONT_COVER,  # Define como capa
            thumbnail_data,  # Dados da imagem
            "image/jpeg"     # Tipo MIME (garantido JPEG)
        )
        audiofile.tag.save()

        # Prepara o arquivo MP3 para envio
        file_stream = io.BytesIO()
        with open(mp3_filename, "rb") as f:
            file_stream.write(f.read())
        file_stream.seek(0)
        os.remove(mp3_filename)  # Remove o arquivo MP3 do disco após o envio

        # Retorna o arquivo MP3 como resposta
        return send_file(file_stream, as_attachment=True, download_name=f"{yt.title}.mp3")
    
    except Exception as e:
        return f"An error occurred: {str(e)}", 500


if __name__ == '__main__':
    app.run(ssl_context='adhoc')
