from PIL import Image, ImageFilter
from tkinter.filedialog import *

file_path = askopenfilename()
image = Image.open(file_path)

# Enhances the image's details.
output_image = image.filter(ImageFilter.DETAIL())
# Sharpens the image.
output_image = image.filter(ImageFilter.SHARPEN())

#Save the resulting image

save_path = asksaveasfilename()
str = save_path + "_noised.jpg"
image.save(str, optimize=True, quality=50)