import os
import sys
from PIL import Image
from colorthief import ColorThief

end = 256
mid = end//2
grid =((0,0,mid,mid),(0,mid,mid,end),(mid,0,end,mid),(mid,mid,end,end))

def palette_folder_maker():
	palette_folder = './palettes'
	
	if os.path.exists(palette_folder) == False:
		os.makedirs(palette_folder)

	return palette_folder

def palette_printer(palette):
	im = Image.new('RGBA',(end,end))
	
	for x in range(4):
		im.paste(palette[x],grid[x])
		
	return im

def palette_maker(directory):
	palette_folder = palette_folder_maker()
	images = [i for i in os.listdir(directory) if os.path.isfile(i) and i.endswith(".jpg")]
	for i in images:
		print(str(images.index(i)+1) + ' of ' + str(len(images)) + ' getting dominant colors for '+str(i))
		iColors =ColorThief(i).get_palette(4)
		im_pallete = palette_printer(iColors)
		im_pallete.save(os.path.join(palette_folder,'palette_'+str(i)))

def pic_smoosher(directory):
	os.chdir(directory)
	palette_list = [i for i in os.listdir('.') if os.path.isfile(i) and i.endswith(".jpg")]

	images = map(Image.open, palette_list)
	widths, heights = zip(*(i.size for i in images))

	total_width = sum(widths)
	max_height = max(heights)

	new_im = Image.new('RGB', (total_width, max_height))

	images = map(Image.open, palette_list)
	x_offset = 0
	for im in images:
	  new_im.paste(im, (x_offset,0))
	  x_offset += im.size[0]

	return new_im

def colourpicker(directory):
	home = os.getcwd()
	directory = os.path.abspath(directory)
	if os.getcwd() != directory:
			os.chdir(directory)
	
	palette_folder = palette_folder_maker()	
	
	palette_maker(directory) #makes palletes for all pictures in thie directory
	
	print('smooshing')
	pic_smoosher(palette_folder).save('combo_pallette.jpg') #smooshes
	
	print('finishing up')
	meta_palette_palette=ColorThief('combo_pallette.jpg').get_palette(4) #works out most prominant colour
	os.chdir(directory)
	palette_printer(meta_palette_palette).save(os.path.join(directory,'1-pallete-of-day.jpg'))
	os.chdir(home)

def main():
	filepath = sys.argv[1]
	colourpicker(filepath)

if __name__ == '__main__':
	main()
