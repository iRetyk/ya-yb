### Run #2 of the python challenge from beginning
# Level 15 - "http://www.pythonchallenge.com/pc/return/uzi.html"

"""
NOTES:
evil 4 is bert
the cat's name i uzi

"""


from PIL import Image

pixels = []
with Image.open("wire.png") as img:
    for x in range(100*100):
        pixels.append(img.getpixel((x,0)))



pixels_2d = [[None for _ in range(100)] for _ in range(100)]

top = 0
bottom = 99
left = 0
right = 99

idx = 0

while top <= bottom and left <= right:
    # left → right
    for col in range(left, right + 1):
        pixels_2d[top][col] = pixels[idx]
        idx += 1
    top += 1

    # top → bottom
    for row in range(top, bottom + 1):
        pixels_2d[row][right] = pixels[idx]
        idx += 1
    right -= 1

    # right → left
    if top <= bottom:
        for col in range(right, left - 1, -1):
            pixels_2d[bottom][col] = pixels[idx]
            idx += 1
        bottom -= 1

    # bottom → top
    if left <= right:
        for row in range(bottom, top - 1, -1):
            pixels_2d[row][left] = pixels[idx]
            idx += 1
        left += 1


with Image.new("RGB", (100, 100)) as img:
    for x in range(100):
        for y in range(100):
            img.putpixel((x, y), pixels_2d[y][x])
    img.save("wire_solved.png")