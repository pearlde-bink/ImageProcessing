from PIL import Image
from tkinter.filedialog import *

file_path = askopenfilename()
img = Image.open(file_path)

width, height = img.size
new_size = (width//2, height//2)
resized_img = img.resize(new_size)

save_path = asksaveasfilename()
str = save_path + "_shrinked.jpg"
resized_img.save(str)

print("new size: ", resized_img.size)