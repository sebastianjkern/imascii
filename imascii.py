import argparse

import PIL.ImageOps
import numpy as np
from PIL import Image
from PIL import ImageEnhance


def get_average_l(image):
    im = np.array(image)
    w, h = im.shape
    return np.average(im.reshape(w * h))


def convert_image_to_ascii(file_name, cols, scale, more_levels, invert, enhance):
    hr_ascii_table = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    lr_ascii_table = '@%#*+=-:. '

    image = Image.open(file_name).convert('L')

    if enhance:
        image = PIL.ImageEnhance.Contrast(image).enhance(3)
        image = PIL.ImageEnhance.Brightness(image).enhance(0.85)

    if invert:
        image = PIL.ImageOps.invert(image)

    original_width, original_height = image.size[0], image.size[1]

    new_width = original_width / cols
    new_height = new_width / scale

    rows = int(original_height / new_height)

    if cols > original_width or rows > original_height:
        exit(0)

    ascii_image = []
    for j in range(rows):
        y1 = int(j * new_height)
        y2 = int((j + 1) * new_height)
        if j == rows - 1:
            y2 = original_height
        ascii_image.append("")

        for i in range(cols):
            x1 = int(i * new_width)
            x2 = int((i + 1) * new_width)
            if i == cols - 1:
                x2 = original_width

            img = image.crop((x1, y1, x2, y2))
            avg = int(get_average_l(img))

            if more_levels:
                greyscale_value = hr_ascii_table[int((avg * 69) / 255)]
            else:
                greyscale_value = lr_ascii_table[int((avg * 9) / 255)]

            ascii_image[j] += greyscale_value

    return ascii_image


def main():
    parser = argparse.ArgumentParser(description="Converts an image into ASCII art.")
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')
    parser.add_argument('--invert', dest='invert', action='store_true')
    parser.add_argument('--enhance', dest='enhance', action='store_true')

    args = parser.parse_args()

    imgFile = args.imgFile

    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile

    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    cols = 80
    if args.cols:
        cols = int(args.cols)

    aimg = convert_image_to_ascii(imgFile, cols, scale, args.moreLevels, args.invert, args.enhance)
    f = open(outFile, 'w')
    for row in aimg:
        f.write(row + '\n')
    f.close()

    for row in aimg:
        print(row)


if __name__ == '__main__':
    main()
