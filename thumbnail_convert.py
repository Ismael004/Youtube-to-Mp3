from PIL import Image
from io import BytesIO
import requests

def thumbnail_convert_jpeg(thumbnail_link):
    response = requests.get(thumbnail_link, stream=True)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))

        image_converted = BytesIO()
        image.convert("RGB").save(image_converted, format="JPEG")
        image_converted.seek(0)
        
        return image_converted.read()
    else:
        return None
