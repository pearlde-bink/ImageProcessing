from PIL import Image, ImageFilter
from tkinter.filedialog import *

file_path = askopenfilename()
image = Image.open(file_path)

# Converting the image to grayscale, as edge detection 
# requires input image to be of mode = Grayscale (L)
image = image.convert("L")

# # Detecting Edges on the Image using the argument ImageFilter.FIND_EDGES
# image = image.filter(ImageFilter.EDGE_ENHANCE)
image = image.filter(ImageFilter.FIND_EDGES())

save_path = asksaveasfilename()
str = save_path + "_edge.jpg"
image.save(str, optimize=True, quality=50)
