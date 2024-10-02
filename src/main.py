# KiryxaTech 2024, MIT License

from PIL import Image
from loader import Loader


def main():
    image_str = Loader.dump_image(Image.open("bin_0.png"))
    image_obj: Image = Loader.load_image(image_str)

    print(image_obj)

if __name__ == "__main__":
    main()