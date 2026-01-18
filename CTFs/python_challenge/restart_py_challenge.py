### Run #2 of the python challenge from beginning
# Level 13 - "http://www.pythonchallenge.com/pc/return/disproportional.html"

from PIL import Image
import io


with open('evil2.gfx','rb') as f:
    raw = f.read()

files = [b'' for _ in range(5)]

for i, byte in enumerate(raw):
    files[i % 5] += bytes([byte])


for file in files:
    try:
        im = Image.open(io.BytesIO(file))
        im.load()
        im.save(f"evil2_result{files.index(file)}.png")
    except Exception as e:
        print(e)