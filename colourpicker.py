#! /env/bin/python3

import os
import sys
from PIL import Image
from colorthief import ColorThief

end = 256
mid = end//2
grid =((0,0,mid,mid),(0,mid,mid,end),(mid,0,end,mid),(mid,mid,end,end)) # initialises the 4x4 grid that the palettes get printed as

def palette_folder_maker(): #makes the subdirectory that contains the palettes
	palette_folder = os.path.join('.','palettes')
	
	if os.path.exists(palette_folder) == False:
		os.makedirs(palette_folder)

	return palette_folder

def palette_printer(palette): #saves a 4x4 grid of the 4 colours from a palette provided to it
	im = Image.new('RGBA',(end,end))
	
	for x in range(4):
		im.paste(palette[x],grid[x])		
	return im

def palette_maker(image_to_average, palette_file_name): #uses ColorThief to make a Palette of the 4 most dominant colours in the images provided to it, saves them in the palette folder

	iColors =ColorThief(image_to_average).get_palette(4) #creates a list of 4 tuples containing the RBG values of the 4 most dominant colours, see ColorThief docs for more info
	im_pallete = palette_printer(iColors)
	im_pallete.convert('RGB').save(palette_file_name)

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

def colourpicker(directory):	# returns a 4x4 palette of the dominant colours of all the pictures in a directory. It creates a 4x4 palette of each image, combines them, and works out the 4 most dominant colors from the combo image
	directory = os.path.abspath(directory)
	os.chdir(directory)
	palette_folder = palette_folder_maker()
	combo_pallette = os.path.join(directory, palette_folder,'combo_pallette.jpg')
	pallette_of_the_day = os.path.join(directory,'1-pallete-of-day.jpg')

	print('Going through the directory')
	images = [i for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and i.endswith(".jpg")]
	for c,i in enumerate(images,1):
		print(c, 'of', len(images),'getting dominant colors for',i)
		palette_file_name = os.path.join(palette_folder,'palette_'+ os.path.basename(i)) 
		palette_maker(i , palette_file_name) #makes palletes for all pictures in thie directory	
	
	print('Smooshing...')
	palette_list = [os.path.join(palette_folder,i) for i in os.listdir(palette_folder) if os.path.isfile(os.path.join(palette_folder,i)) and i.endswith(".jpg")]
	pic_smoosher(palette_list).save(combo_pallette) #smooshes
	
	print('Palettes smooshed, finding dominant colour across all palettes')
	palette_maker(combo_pallette, pallette_of_the_day)


def main(): #stand-alone version for debugging, directory taken from command line
	filepath = sys.argv[1]
	colourpicker(filepath)

if __name__ == '__main__':
	main()