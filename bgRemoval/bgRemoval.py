from PIL import Image
from rembg import remove
import os
from tkinter.filedialog import *

file_path = askopenfilename()
image = Image.open(file_path)

bg_image = remove(image)

save_path = asksaveasfilename()
str = save_path + "_bgremove.png"
bg_image.save(str, optimize=True, quality=50)

print("Oke")