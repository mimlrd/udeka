## saving pictures and other items
import os
from PIL import Image



## Saving the picture to database function
def save_picture(form_picture):
	## let change the name for the picture to random number
	random_hex = secrets.token_hex(8)
	## to get the extension and the picture filename
	##f_name , f_ext = os.path.splitext(form_picture.filename)
	## replace f_name with "_" as we are not using the variable
	_, f_ext = os.path.splitext(form_picture.filename)
	## create the new name for the picture
	new_filename = random_hex + f_ext
	## get the path to save the picture
	picture_path = os.path.join(app.root_path, 'static/profile_img', new_filename)

	## Let resize the picture before we save it
	## let get the turple of the output size that we want
	output_size = (125,125)
	## create a new image - First open the image to resize, then resize
	img = Image.open(form_picture)
	img.thumbnail(output_size)

	## letsave the picture
	img.save(picture_path)

	## Let reurn the picture path so we can work with it outsite this function
	return new_filename
