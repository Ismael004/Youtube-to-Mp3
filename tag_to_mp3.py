import eyed3
import thumbnail_convert

def tag_insert(yt):
    thumbnail_data = thumbnail_convert.thumbnail_convert_jpeg(yt.thumbnail_url)
    mp3_file_eyed = eyed3.load(f"{yt.title}.mp3")

    if mp3_file_eyed.tag is None:
        mp3_file_eyed.initTag()

    mp3_file_eyed.tag.artist = yt.author 
    mp3_file_eyed.tag.title = yt.title 
    mp3_file_eyed.tag.images.set(
            eyed3.id3.frames.ImageFrame.FRONT_COVER,  # Define como capa
            thumbnail_data,  # Dados da imagem
            "image/jpeg"     # Tipo MIME (garantido JPEG)
        )
    mp3_file_eyed.tag.save()

