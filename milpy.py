#! /env/bin/python3

# M(att's) I(mage) L(ibrary) is a collection of my image processes that i've developed

import os
import sys
from PIL import Image
from colorthief import ColorThief

def folder_maker(directory,folder_name):
	folder = os.path.join(directory,folder_name)

	if os.path.exists(folder) == False:
		os.mkdirs(folder)

	return folder

def grid_printer(colors, size):
	
	mid = size//2
 	grid =((0,0,mid,mid),(0,mid,mid,size),(mid,0,size,mid),(mid,mid,size,size))
	
	im = Image.new('RGB',(size,size))
		for x in range(4):
		im.paste(colors[x],grid[x])

	return im

def palette_maker(image_to_average, palette_size): # uses ColorThief to make a palette of the 4 most dominant colors in the image provided to it, returns a new image file of a 2x2 grid of those colors 
	image_colors = ColorThief(image_to_average).get_palette(4) # creates a list of 4 tuples containing the RBG values of the 4 most dominant colours, see ColorThief docs for more info
	im_pallete = grid_printer(image_colors, palette_size) 
	
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

def bulk_picture_resizer(images_to_shrink, target_directory, target_height):	
	for picture in images_to_shrink:
		img = Image.open(picture)
		w , h = img.size
		ratio = h / target_height
		resized_img = img.resize((int(w/ratio),int(h/ratio)))
		resized_img.convert('RGB').save(os.path.join(target_directory,'shrunk_' + os.path.basename(picture))



shrunk_folder = folder_maker(directory)
files = [os.path.join(directory,i) for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and i.endswith(".jpg")]