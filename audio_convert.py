from pytubefix import YouTube
from pydub import AudioSegment
import os
from io import BytesIO

def convert_to_mp3(yt):
    stream_audio = yt.streams.filter(only_audio=True).first()

    audio_file = stream_audio.download(filename=f"{yt.title}")

    mp3_filename = f"{yt.title}.mp3" 
    song_Audio = AudioSegment.from_file(audio_file)
    song_Audio.export(mp3_filename, format="mp3")
    
    os.remove(audio_file)

    


