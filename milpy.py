#! /.env/bin/python3

# M(att's) I(mage) L(ibrary) PY(thon) is a collection of my image processes that i've developed

import os
from PIL import Image
from colorthief import ColorThief

def folder_maker(directory,folder_name):
	folder = os.path.join(directory,folder_name)

	if os.path.exists(folder) == False:
		os.mkdir(folder)

	return folder

def get_images_in_dir(directory , filetype):
	images = [os.path.join(directory,i) for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and i.endswith(filetype)]

	return images

def grid_printer(colors, size):
	mid = size//2
	grid =((0,0,mid,mid),(0,mid,mid,size),(mid,0,size,mid),(mid,mid,size,size))
	
	im = Image.new('RGB',(size,size))
	for x in range(4):
		im.paste(colors[x],grid[x])

	return im


def average_colors(image_to_average): # uses ColorThief to make a palette of the 4 most dominant colors in the image provided to it, returns a new image file of a 2x2 grid of those colors 
	image_colors = ColorThief(image_to_average).get_palette(4) # creates a list of 4 tuples containing the RBG values of the 4 most dominant colors, see ColorThief docs for more info
	im_pallete = grid_printer(image_colors, 256) 
	
	return im_pallete

def pic_smoosher(images_to_smoosh): # combines multiple images into one big long image, currently only really works if the images provided are the same height & width
	images = map(Image.open, images_to_smoosh)
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	images = map(Image.open, images_to_smoosh)
	x_offset = 0

	for im in images:
	  new_im.paste(im, (x_offset,0))
	  x_offset += im.size[0]

	return new_im

def bulk_picture_resizer(images_to_shrink, save_location, target_height):		
	for count, picture in enumerate(images_to_shrink,1):
		img = Image.open(picture)
		w , h = img.size
		ratio = h / target_height
		print(count, 'of', len(images_to_shrink),'shrinking',picture)
		resized_img = img.resize((int(w/ratio),int(h/ratio)))
		resized_img.convert('RGB').save(os.path.join(save_location,'shrunk_' + os.path.basename(picture)))

def multi_image_average(images_to_average):
	home_folder = os.path.dirname(images_to_average[0])
	save_location = folder_maker(home_folder,'shrunk')
	combined_image_filename = os.path.join(save_location,'combined_image.jpg')
	average_pallete_filename = os.path.join(home_folder,'1_average_colors.jpg')

	print('Shrinking pictures')
	bulk_picture_resizer(images_to_average, save_location, 256)
	
	shrunk_images = get_images_in_dir(save_location , '.jpg')

	print('Combining shrunken images')
	combined_images = pic_smoosher(shrunk_images)
	combined_images.save(combined_image_filename)

	print('Finding average color of combined image')
	combined_image_palette = average_colors(combined_image_filename)
	combined_image_palette.save(average_pallete_filename)

def directory_image_average(directory, filetype):
	images = get_images_in_dir(directory, filetype)
	multi_image_average(images)

'''
shrunk_folder = folder_maker(directory)
files = [os.path.join(directory,i) for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and i.endswith(".jpg")]
'''