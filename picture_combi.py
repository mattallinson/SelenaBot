import os
from PIL import Image
import colourpicker as cp
from colorthief import ColorThief

target_height = 256

def shrunk_folder_maker(directory): #makes the subdirectory that contains the shrunken images
	shrunk_folder = os.path.join(directory,'shrunk')
	
	if os.path.exists(shrunk_folder) == False:
		os.makedirs(shrunk_folder)

	return shrunk_folder

def picture_resizer(directory):	
	shrunk_folder = shrunk_folder_maker(directory)
	files = [os.path.join(directory,i) for i in os.listdir(directory) if os.path.isfile(os.path.join(directory,i)) and i.endswith(".jpg")]
	for f in files:
		img = Image.open(f)
		w , h = img.size
		ratio = h / target_height
		resized_img = img.resize((int(w/ratio),int(h/ratio)))
		resized_img.save(os.path.join(shrunk_folder,'shrunk',f))

def picture_combi(directory):
	directory = os.path.abspath(directory)
	shrunk_folder = shrunk_folder_maker(directory)
	picture_resizer(directory)
	cp.pic_smoosher(shrunk_folder).save(os.path.join(directory, shrunk_folder,'combo_picture.jpg'))
	combi_palette = ColorThief(os.path.join(directory, shrunk_folder,'combo_picture.jpg')).get_palette(4)
	cp.palette_printer(meta_palette_palette).save(os.path.join(directory,'2-pallete-of-day.jpg'))

def main(): #stand-alone version for debugging, directory taken from command line
	filepath = sys.argv[1]
	picture_combi(filepath)

if __name__ == '__main__':
	main()