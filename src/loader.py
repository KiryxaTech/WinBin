import io
import base64
import PIL.Image

class Loader:
    @staticmethod
    def load_image(image_str: str) -> PIL.Image:

        image_bytes = base64.b64decode(image_str)
        image = PIL.Image.open(io.BytesIO(image_bytes))

        return image
    
    @staticmethod
    def dump_image(image: PIL.Image) -> str:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_str = base64.b64encode(buffered.getvalue()).decode()

        return image_str