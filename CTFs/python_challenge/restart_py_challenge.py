### Run #2 of the python challenge from beginning
# Level 16 - "http://www.pythonchallenge.com/pc/return/mozart.html"

"""
NOTES:
evil 4 is bert
the cat's name i uzi

"""
from PIL import Image

img = Image.open("mozart.gif")
img = img.convert("RGB")
pixels = list(img.getdata()) 

width, height = img.size
pixels_2d = [pixels[i * width:(i + 1) * width] for i in range(height)]

white_index = []

for j in range(height):
    for i in range(width):
        if pixels_2d[j][i] > (240, 240, 240):
            white_index.append(i)
            break
new_pixels_2d = [[None for _ in range(width)] for _ in range(height)]

for j in range(height):
    shift = white_index[j]
    new_pixels_2d[j] = pixels_2d[j][shift:] + pixels_2d[j][:shift]

new_pixels = [pixel for row in new_pixels_2d for pixel in row]
new_img = Image.new("RGB", (width, height))
new_img.putdata(new_pixels)
new_img.save("mozart_solved.gif")