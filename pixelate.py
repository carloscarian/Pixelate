from PIL import Image

from tkinter import Tk
from tkinter.filedialog import askopenfilename

#REDO FROM SCRATCH WITH HSV PROBABLY
#NEED TO CLEAN EVERYTHING UP, THIS IS A MESS


def palette_reduction(img_orig, n):
    # this function reduce the color palette used in an image
    # img is the image file path
    # n is a number from 2 to 127 that determines how big the new palette is, where 2 is the biggest and 127 is the smallest
    px_orig = img_orig.load()
    width_orig, height_orig = img_orig.size
    img_new = Image.new("RGB", (width_orig, height_orig))
    px_new = img_new.load()
    for i in range(width_orig):
        for j in range(height_orig):
            color = list(px_orig[i, j])
            for k in range(3):
                color[k] = n*(round(color[k]/n))
            px_new[i, j] = tuple(color)
    return(img_new)

print("Choose the file to pixelate: ")

Tk().withdraw()

path = askopenfilename(filetypes=[("Image files", "*.png"), ("Image files", "*.jpg"), ("All Files", "*.*")])

img_orig = Image.open(path)

px_orig = img_orig.load()

width_orig, height_orig = img_orig.size

format_orig = img_orig.format

big_pixel_size = int(input("Enter new pixel size: "))

# mode = input("Enter conversion mode (mean, median): ")

crop_flag = int(
    input(
        "There are three ways to make the big pixels fit: \n"
        "1) crop the image at the end \n"
        "2) have smaller big pixels at the edges \n"
        "Input 1 or 2 to confirm your choice:"
    )
)

print("Converting...")

if crop_flag == 1:
    bigpixel_amount_x = width_orig // big_pixel_size
    bigpixel_amount_y = height_orig // big_pixel_size
    img_new = Image.new("RGB", (bigpixel_amount_x*big_pixel_size, bigpixel_amount_y*big_pixel_size))
    px_new = img_new.load()
    for i in range(0, bigpixel_amount_x):
        for j in range(0, bigpixel_amount_y):
            # this does arithmetic mean and avoids possible
            # overflow by not doing the sum in one go
            counter = 1
            mean_pixel_color = px_orig[i * big_pixel_size, j * big_pixel_size]
            for l in range(0, big_pixel_size):
                for m in range(0, big_pixel_size):
                    mean_pixel_color = tuple(
                        [(x * counter) / (counter + 1) for x in mean_pixel_color]
                    )
                    new_color = tuple(
                        [
                            x / (counter + 1)
                            for x in px_orig[
                                i * big_pixel_size + l, j * big_pixel_size + m
                            ]
                        ]
                    )
                    updated_color = [
                        int(mean_pixel_color[n] + new_color[n]) for n in range(3)
                    ]
                    mean_pixel_color = tuple(updated_color)
                    counter += 1
            for l in range(0, big_pixel_size):
                for m in range(0, big_pixel_size):
                    px_new[
                        int(i * big_pixel_size + l), int(j * big_pixel_size + m)
                    ] = mean_pixel_color

if crop_flag == 2:
    bigpixel_amount_x = width_orig // big_pixel_size
    bigpixel_amount_y = height_orig // big_pixel_size
    remainder_x = width_orig % big_pixel_size
    remainder_y = height_orig % big_pixel_size
    img_new = Image.new("RGB", (width_orig, height_orig))
    px_new = img_new.load()
    for i in range(0, bigpixel_amount_x):
        for j in range(0, bigpixel_amount_y):
            counter = 1
            mean_pixel_color = px_orig[i * big_pixel_size, j * big_pixel_size]
            for l in range(0, big_pixel_size):
                for m in range(0, big_pixel_size):
                    mean_pixel_color = tuple(
                        [(x * counter) / (counter + 1) for x in mean_pixel_color]
                    )
                    new_color = tuple(
                        [
                            x / (counter + 1)
                            for x in px_orig[
                                i * big_pixel_size + l, j * big_pixel_size + m
                            ]
                        ]
                    )
                    updated_color = [
                        int(mean_pixel_color[n] + new_color[n]) for n in range(3)
                    ]
                    mean_pixel_color = tuple(updated_color)
                    counter += 1
            for l in range(0, big_pixel_size):
                for m in range(0, big_pixel_size):
                    px_new[
                        int(i * big_pixel_size + l), int(j * big_pixel_size + m)
                    ] = mean_pixel_color

    for i in range(0, bigpixel_amount_x):
        counter = 1
        mean_pixel_color = px_orig[i * big_pixel_size, bigpixel_amount_y * big_pixel_size]
        for l in range(0, big_pixel_size):
            for m in range(0, remainder_y):
                mean_pixel_color = tuple(
                    [(x * counter) / (counter + 1) for x in mean_pixel_color]
                )
                new_color = tuple(
                    [
                        x / (counter + 1)
                        for x in px_orig[
                            i * big_pixel_size + l, bigpixel_amount_y * big_pixel_size + m
                        ]
                    ]
                )
                updated_color = [
                    int(mean_pixel_color[n] + new_color[n]) for n in range(3)
                ]
                mean_pixel_color = tuple(updated_color)
                counter += 1
        for l in range(0, big_pixel_size):
            for m in range(0, remainder_y):
                px_new[
                    int(i * big_pixel_size + l), int(bigpixel_amount_y * big_pixel_size + m)
                ] = mean_pixel_color

    for j in range(0, bigpixel_amount_y):
        counter = 1
        mean_pixel_color = px_orig[bigpixel_amount_y * big_pixel_size, j * big_pixel_size]
        for l in range(0, remainder_x):
            for m in range(0, big_pixel_size):
                mean_pixel_color = tuple(
                    [(x * counter) / (counter + 1) for x in mean_pixel_color]
                )
                new_color = tuple(
                    [
                        x / (counter + 1)
                        for x in px_orig[
                            bigpixel_amount_x * big_pixel_size + l,  j * big_pixel_size + m
                        ]
                    ]
                )
                updated_color = [
                    int(mean_pixel_color[n] + new_color[n]) for n in range(3)
                ]
                mean_pixel_color = tuple(updated_color)
                counter += 1
        for l in range(0, remainder_x):
            for m in range(0, big_pixel_size):
                px_new[
                    int(bigpixel_amount_x * big_pixel_size + l), int(j * big_pixel_size + m)
                ] = mean_pixel_color

img_new1 = palette_reduction(img_new, 5)
img_new2 = palette_reduction(img_new, 10)
img_new3 = palette_reduction(img_new, 15)

#anti-anti-aliasing
#find isolated pixels and kill them
for i in range(1, bigpixel_amount_x - 1):
    for j in range(1, bigpixel_amount_y - 1):
        colorhere = px_new[int(big_pixel_size*i), int(big_pixel_size*j)]
        isolated_flag1 = (px_new[int(big_pixel_size*(i + 1)), int(big_pixel_size*j)] != colorhere)
        isolated_flag2 = (px_new[int(big_pixel_size*(i - 1)), int(big_pixel_size*j)] != colorhere)
        isolated_flag3 = (px_new[int(big_pixel_size*i), int(big_pixel_size*(j + 1))] != colorhere)
        isolated_flag4 = (px_new[int(big_pixel_size*i), int(big_pixel_size*(j - 1))] != colorhere)
        isolated_flag = isolated_flag1 and isolated_flag2 and isolated_flag3 and isolated_flag4
        if isolated_flag == False:
            color1 = px_new[int(big_pixel_size*(i + 1)), int(big_pixel_size*j)]
            color2 = px_new[int(big_pixel_size*(i - 1)), int(big_pixel_size*j)]
            color3 = px_new[int(big_pixel_size*i), int(big_pixel_size*(j + 1))]
            color4 = px_new[int(big_pixel_size*i), int(big_pixel_size*(j - 1))]
            mean_color = tuple([int((color1[i] + color2[i] + color3[i] + color4[i])/4) for i in range(3)])
            for l in range(big_pixel_size):
                for m in range(big_pixel_size):
                    px_new[int(i*big_pixel_size + l), int(j*big_pixel_size + m)] = mean_color


print("Done! :)")
img_new.show()
img_new1.show()
img_new2.show()
img_new3.show()
