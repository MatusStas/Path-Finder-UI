from PIL import Image, ImageDraw
from getch import getch
from tkinter import *
import time
import PIL

color = 'red'
on = 0
start_block_on = 0

arr_color = {}

def set_size():
	width = 60
	height = 25
	pixel_size = 30
	return width*pixel_size, height*pixel_size, pixel_size


def create_grid(width, height, pixel_size):
	for row in range(pixel_size, height, pixel_size):
		screen.create_line(0, row, width, row, fill = "grey")
	for column in range(pixel_size, width, pixel_size):
		screen.create_line(column, 0, column, height, fill = "grey")


def set_color(colour):
	global color
	color = colour


def paint(event):
	global color, start_block_on, arr_color
	if color == 'white':
		x1, y1 = (event.x)//pixel_size, (event.y)//pixel_size
		screen.create_rectangle(x1*pixel_size+1, y1*pixel_size+1, x1*pixel_size+pixel_size-1, y1*pixel_size+pixel_size-1, fill = color, outline = color)
		draw.rectangle([x1*pixel_size+1, y1*pixel_size+1, x1*pixel_size+pixel_size-1, y1*pixel_size+pixel_size-1], fill = color, outline = color)
		start_block_on = 1
		if (x1,y1) in arr_color:
			clr = arr_color[(x1,y1)]
			print(clr)
			if clr == "red" and start_block_on == 1:
				start_block_on = 0
	elif not(start_block_on == 1 and color == 'red'):
		x1, y1 = (event.x)//pixel_size, (event.y)//pixel_size
		screen.create_rectangle(x1*pixel_size+1, y1*pixel_size+1, x1*pixel_size+pixel_size-1, y1*pixel_size+pixel_size-1, fill = color, outline = color)
		draw.rectangle([x1*pixel_size+1, y1*pixel_size+1, x1*pixel_size+pixel_size-1, y1*pixel_size+pixel_size-1], fill = color, outline = color)
		start_block_on = 1
		arr_color[(x1,y1)] = "red"
		print(arr_color)




def pixel_color(x, y):
	r, g, b = image.getpixel((x+1, y+1))
	return r, g, b


def erase_all():
	global on, start_block_on
	if not(on):
		for column in range(0, height, pixel_size):
			for row in range(0, width, pixel_size):
				screen.create_rectangle(row+1, column+1, row+pixel_size-1, column+pixel_size-1, fill = 'white', outline = 'white')
				draw.rectangle([row+1, column+1, row+pixel_size-1, column+pixel_size-1], fill = 'white', outline = 'white')
	start_block_on = 0

def make():																		
	arr = []
	count = 0
	for row in range(0, width, pixel_size):
		arr.append([])
		for column in range(0, height, pixel_size):
			arr[row//pixel_size].append(0)

			if(pixel_color(row, column) == (255, 0, 0)):
				start = [row, column]
				count += 1
			if(pixel_color(row, column) == (0, 0, 255)):
				end = [row, column]
				count += 1

	return arr, start, end


def poinf_info(x, y):
	info = []
	if(not(y-pixel_size < 0) and pixel_color(x, y-pixel_size) != (0, 0, 0) and pixel_color(x, y-pixel_size) != (128, 128, 128)):
		info.append([x, y-pixel_size])
	if(not(x+pixel_size+1 > width) and pixel_color(x+pixel_size, y) != (0, 0, 0) and pixel_color(x+pixel_size, y) != (128, 128, 128)):
		info.append([x+pixel_size, y])
	if(not(y+pixel_size+1 > height) and pixel_color(x, y+pixel_size) != (0, 0, 0) and pixel_color(x, y+pixel_size) != (128, 128, 128)):
		info.append([x, y+pixel_size])
	if(not(x-pixel_size < 0) and pixel_color(x-pixel_size, y) != (0, 0, 0) and pixel_color(x-pixel_size, y) != (128, 128, 128)):
		info.append([x-pixel_size, y])
	return info


def execute():
	global on
	arr, start, end = make()
	que = [start]

	x_start, y_start = start
	S = [x_start//pixel_size, y_start//pixel_size]

	x_end, y_end = end
	E = [x_end, y_end]
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
				x, y = arr_of_visiting[element]
				arr[x//pixel_size][y//pixel_size] = [que[0][0]//pixel_size, que[0][1]//pixel_size]

				if(S != [x//pixel_size, y//pixel_size] and E != [x, y]):
					screen.create_rectangle(x+1, y+1, x+pixel_size-1, y+pixel_size-1, fill = "grey")
					draw.rectangle([x+1, y+1, x+pixel_size-1, y+pixel_size-1], fill = "grey", outline = "grey")
					
					screen.update()
					time.sleep(0.001)
		que.pop(0)

	E = arr[x_end//pixel_size][y_end//pixel_size]
	step = 0
	walker = E

	while(walker != S):
		on = 1
		x = walker[0]
		y = walker[1]
		screen.create_rectangle(x*pixel_size+1, y*pixel_size+1, x*pixel_size+pixel_size-1, y*pixel_size+pixel_size-1, fill = "light goldenrod", outline = "light goldenrod")
		walker = arr[walker[0]][walker[1]]
		
		screen.update()
		time.sleep(0.1)
		step += 1
	on = 0



width, height, pixel_size = set_size()

root = Tk()
root.resizable(False, False)
root.geometry(f'{width}x{height+52}')
root.title("P A T H    F I N D E R")

screen = Canvas(root, width = width, height = height, bg = "white")
screen.pack(side="top")

image = PIL.Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(image)

create_grid(width, height, pixel_size)

screen.bind("<Button-1>", paint)
screen.bind("<B1-Motion>", paint)

but_exe = Button(root, width = 33, height = 2, text = "EXECUTE", command = execute).place(x = 2, y = height+2)
but_str = Button(root, width = 33, height = 2, text = "START BLOCK", command = lambda: set_color('red')).place(x = 303, y = height+2)
but_fin = Button(root, width = 33, height = 2, text = "FINISH BLOCK", command = lambda: set_color('blue')).place(x = 604, y = height+2)
but_obs = Button(root, width = 33, height = 2, text = "OBSTACLE BLOCK", command = lambda: set_color('black')).place(x = 905, y = height+2)
but_era = Button(root, width = 33, height = 2, text = "ERASE BLOCK", command = lambda: set_color('white')).place(x = 1206, y = height+2)
but_all = Button(root, width = 33, height = 2, text = "ERASE ALL", command = erase_all).place(x = 1506, y = height+2)

root.mainloop()