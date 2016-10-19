from PIL import Image
import argparse
from os.path import exists, splitext


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('imagepath', help='Путь к исходной картинке')
    parser.add_argument('-w', '--width', type=int)
    parser.add_argument('-H', '--height', type=int)
    parser.add_argument('-s', '--scale', type=float)
    parser.add_argument('-o', '--output')
    return parser


def open_image(path_to_original):
    return Image.open(path_to_original)


def not_scale(image, new_width, new_height):
    width, height = image.size
    if new_height:
        new_width = round(new_height / height * width)
    elif new_width:
        new_height = round(new_width / width * height)
    return image.resize((new_width, new_height))


def scale_image(image, scale):
    width, height = image.size
    result_size = (round(width * scale), round(height * scale))
    return image.resize(result_size)


def resize_image(image, new_width, new_height):
    width, height = image.size
    if round(width / height, 4) != round(new_width / new_height, 4):
        print('WARNING: image scale is not respected')
    return image.resize((new_width, new_height))


def save_image(image, source_path, path_to_result):
    if path_to_result:
        image.save(path_to_result, image.format)
        return True
    widht, height = image.size
    base, ext = splitext(source_path)
    path_to_result = '{}__{}x{}{}'.format(base, widht, height, ext)
    image.save(path_to_result, image.format)


if __name__ == '__main__':
    parser = createParser()
    ns = parser.parse_args()
    if ns.scale and any([ns.height, ns.width]):
        parser.error('should be either --scale or [--width or --height]')
    if not exists(ns.imagepath):
        parser.error('{} doesn\'t exist!'.format(ns.imagepath))
    img = open_image(ns.imagepath)
    if ns.scale:
        img = scale_image(img, ns.scale)
    elif ns.width and ns.height:
        img = resize_image(img, ns.width, ns.height)
    elif ns.width or ns.height:
        img = not_scale(img, ns.width, ns.height)
    save_image(img, ns.imagepath, ns.output)
