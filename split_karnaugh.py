from PIL import Image
import os

img = Image.open("karnaughs inversed.png")

y_offset = 0
for i in range(0, 7):
    cropped = img.crop((0, y_offset, 289, y_offset + 149))
    cropped.save(f"cropped\\{i}.png")
    y_offset += 149
    y_offset += 11
