## saving pictures and other items
import os
import secrets
import io
# import cStringIO
from PIL import Image
#from eduka import s3
from app import app
import boto3


## Saving the picture to database function
def resize_picture(form_picture):

	image_types = {
    'jpg': 'JPEG',
	'jpeg': 'JPEG',
    'png': 'PNG',
    'gif': 'GIF',
    'tif': 'TIFF'
	}
	## let change the name for the picture to random number
	random_hex = secrets.token_hex(8)
	## to get the extension and the picture filename
	##f_name , f_ext = os.path.splitext(form_picture.filename)
	## replace f_name with "_" as we are not using the variable
	_, f_ext = os.path.splitext(form_picture.filename)

	## create the new name for the picture
	new_filename = random_hex + f_ext
	## Let resize the picture before we save it
	## let get the turple of the output size that we want
	output_size = (125,125)
	## create a new image - First open the image to resize, then resize
	#Load the URL data into an image

	thumbnail_image = Image.open(form_picture)
	i_width, i_height = thumbnail_image.size
	if i_width > output_size[1]:
		'''
		Only resize the picture if the width is greater than the output width
		'''

		## prepare the buffer
		buffer = io.BytesIO()

		thumbnail_image.thumbnail(output_size, Image.ANTIALIAS)
		## Let get the file suffix to save the format in the buffer
		filename_suffix = f_ext[1:]
		image_format = image_types[filename_suffix]

		# You must tell PIL which format to use because there is no
	    # filename in the .save() call for it to guess from, since
	    # we are saving the thumbnail data to a virtual buffer.

	    # we save the image data into the buffer
		thumbnail_image.save(buffer, format=image_format)

		## Let reurn the picture path so we can work with it outsite this function
		return (new_filename, buffer.getvalue())

	else:
		return (new_filename, form_picture)





def upload_file_to_s3(file, acl="public-read"):

	new_filename, img_byte = resize_picture(file)

	bucket_name = app.config["FLASKS3_BUCKET_NAME"]
	# print(f' bucket name: {bucket_name}')

	s3 = boto3.resource(
	   "s3",
	   aws_access_key_id=app.config["AWS_ACCESS_KEY_ID"],
	   aws_secret_access_key=app.config["AWS_SECRET_ACCESS_KEY"]
	)
	url = ""
	try:

		avatar_filepath = "user-profile-images/"
		key = f"{avatar_filepath}{new_filename}"
		s3.Bucket(bucket_name).put_object(Key=key, Body=img_byte, ACL='public-read')
		location = boto3.client('s3').get_bucket_location(Bucket=bucket_name)['LocationConstraint']
		#location = app.config["FLASKS3_REGION"]
		url = f"https://s3-{location}.amazonaws.com/{bucket_name}/{key}"
		#print(f"url: {url}")

	except Exception as e:
		print("Something Happened: ", e)
		return e

	return url
