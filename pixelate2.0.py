from PIL import Image

from tkinter import Tk
from tkinter.filedialog import askopenfilename

def palette_reduction(img_orig, n):
    # this function reduce the color palette used in an image
    # img is the image file path
    # n is a number from 2 to 127 that determines how big the new palette is, where 2 is the biggest and 127 is the smallest
    px_orig = img_orig.load()
    width_orig, height_orig = img_orig.size
    img_new = Image.new("HSV", (width_orig, height_orig))
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

big_pixel_size = int(input("Enter new pixel size: "))

img_orig = Image.open(path)

px_orig = img_orig.load()

width_orig, height_orig = img_orig.size

width_new = width_orig//big_pixel_size
height_new = height_orig//big_pixel_size

print("Converting...")

img_new = img_orig.resize((width_new, height_new))

print("Done! :)")

img_new.show()
