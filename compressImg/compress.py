from PIL import Image
import os
from tkinter.filedialog import *

file_path = askopenfilename()
image = Image.open(file_path)

width, height = image.size
new_size = (width//2, height//2)
resized_image = image.resize(new_size)

save_path = asksaveasfilename()
str = save_path + "_compressed.jpg"
resized_image.save(str, optimize=True, quality=50)

original_size = os.path.getsize(file_path)
compressed_size = os.path.getsize(str)

print("Original Size: ", original_size)
print("Compressed Size: ", compressed_size)