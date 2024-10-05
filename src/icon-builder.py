from PIL import Image

from core.loader import Loader
from core.package import IconPackage, IconPackageManager

images = []
for i in range(4):
    images.append(Loader.dump_image(Image.open(f"bin_{i}.png")))


print(images)