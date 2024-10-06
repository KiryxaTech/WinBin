# KiryxaTech 2024, MIT License

import io
import base64

import PIL.Image
from PIL.Image import Image


class Loader:
    @staticmethod
    def to_image(image_str: str) -> Image:

        image_bytes = base64.b64decode(image_str)
        image = PIL.Image.open(io.BytesIO(image_bytes))

        return image
    
    @staticmethod
    def to_bytes(image: Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_str = base64.b64encode(buffered.getvalue()).decode()

        return image_str