from PIL import Image, ImageDraw
import PIL
from tkinter import *
import time
from getch import getch

# default color
color = 'red'

def set_red():
	global color
	color = 'red'

def set_blue():
	global color
	color = 'blue'

def set_white():
	global color
	color = 'white'

def set_black():
	global color
	color = 'black'

def get_size():
	width = 60
	height = 25
	pixel_size = 30
	return width*pixel_size, height*pixel_size, pixel_size

width, height, pixel_size = get_size()

#this blok is used to drawing all objects in the grid like obstacles, start point, end point, erasing

def paint(event):
	global color		
	x1,y1 = (event.x)//pixel_size, (event.y)//pixel_size
	platno.create_rectangle(x1*pixel_size+1,y1*pixel_size+1,x1*pixel_size+pixel_size-1,y1*pixel_size+pixel_size-1, fill = color, outline = color)
	draw.rectangle([x1*pixel_size+1,y1*pixel_size+1,x1*pixel_size+pixel_size-1,y1*pixel_size+pixel_size-1], fill = color, outline = color)


def pixel_color(x,y):					#getting the color of current pixel in X Y axis
	r,g,b = image.getpixel((x+1,y+1))
	return r,g,b

			

def make():								#makes 2d array defined with 0s => if point was visited then changed to coordinates										
	arr = []							#also function will find start point + end point
	count = 0
	for riadok in range(0,width,pixel_size):
		arr.append([])
		for stlpec in range(0,height,pixel_size):
			arr[riadok//pixel_size].append(0)

			if(pixel_color(riadok,stlpec) == (255,0,0)):
				start = [riadok,stlpec]
				count += 1
			if(pixel_color(riadok,stlpec) == (0,0,255)):
				end = [riadok,stlpec]
				count += 1

	return arr,start,end



def poinf_info(x,y):					#searching for all neighbours
	info = []							#if pixel is black,grey == obstacle,visited pixel == no added to neighbour 
	if(not(y-pixel_size < 0) and pixel_color(x,y-pixel_size) != (0,0,0) and pixel_color(x,y-pixel_size) != (128,128,128)):
		info.append([x,y-pixel_size])
	if(not(x+pixel_size+1 > width) and pixel_color(x+pixel_size,y) != (0,0,0) and pixel_color(x+pixel_size,y) != (128,128,128)):
		info.append([x+pixel_size,y])
	if(not(y+pixel_size+1 > height) and pixel_color(x,y+pixel_size) != (0,0,0) and pixel_color(x,y+pixel_size) != (128,128,128)):
		info.append([x,y+pixel_size])
	if(not(x-pixel_size < 0) and pixel_color(x-pixel_size,y) != (0,0,0) and pixel_color(x-pixel_size,y) != (128,128,128)):
		info.append([x-pixel_size,y])
	return info



def execute():
	arr,start,end = make()
	que = [start]


	x_start,y_start = start
	S = [x_start//pixel_size,y_start//pixel_size]

	x_end, y_end = end
	E = [x_end,y_end]
	i = 0
	while(arr[x_end//pixel_size][y_end//pixel_size] == 0):
		if(len(que) == 0):
			label_no_path = Label(root, text = "NO PATH!")
			label_no_path.pack()
			return 

		arr_of_visiting = poinf_info(*que[0])
		for element in range(len(arr_of_visiting)):
			
			if(arr_of_visiting[element] not in que):
				que.append(arr_of_visiting[element])
				x,y = arr_of_visiting[element]
				arr[x//pixel_size][y//pixel_size] = [que[0][0]//pixel_size,que[0][1]//pixel_size]

				if(S != [x//pixel_size,y//pixel_size] and E != [x,y]):
					platno.create_rectangle(x+1,y+1,x+pixel_size-1,y+pixel_size-1, fill = "grey")
					draw.rectangle([x+1,y+1,x+pixel_size-1,y+pixel_size-1], fill = "grey", outline = "grey")
					
					platno.update()
					time.sleep(0.001)
		que.pop(0)

	
	E = arr[x_end//pixel_size][y_end//pixel_size]
	step = 0
	walker = E

	while(walker != S):
		x = walker[0]
		y = walker[1]
		platno.create_rectangle(x*pixel_size+1,y*pixel_size+1,x*pixel_size+pixel_size-1,y*pixel_size+pixel_size-1, fill = "light goldenrod", outline = "light goldenrod")
		walker = arr[walker[0]][walker[1]]
		
		platno.update()
		time.sleep(0.1)
		step += 1


root = Tk()
root.resizable(False, False)
root.title("P A T H    F I N D E R")
root.geometry(f'{width}x{height+52}')

platno = Canvas(root, width = width, height = height, bg = "white")
platno.pack(side="top")

image = PIL.Image.new("RGB", (width,height), "white")
draw = ImageDraw.Draw(image)

def create_grid(width,height,pixel_size):	#making the grid
	for riadok in range(pixel_size,height,pixel_size):
		platno.create_line(0,riadok,width,riadok, fill = "grey")
	for stlpec in range(pixel_size,width,pixel_size):
		platno.create_line(stlpec,0,stlpec,height, fill = "grey")

create_grid(width,height,pixel_size)

platno.bind("<Button-1>", paint)
platno.bind("<B1-Motion>", paint)

but_exe = Button(root, width = 40, height = 2, text = "EXECUTE", command = execute).place(x = 4, y = height+2)
but_str = Button(root, width = 40, height = 2, text = "START BLOCK", command = set_red).place(x = 365, y = height+2)
but_fin = Button(root, width = 40, height = 2, text = "FINISH BLOCK", command = set_blue).place(x = 726, y = height+2)
but_obs = Button(root, width = 40, height = 2, text = "OBSTACLE BLOCK", command = set_black).place(x = 1087, y = height+2)
but_era = Button(root, width = 40, height = 2, text = "ERASE", command = set_white).place(x = 1448, y = height+2)

root.mainloop()