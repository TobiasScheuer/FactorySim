import pygame
from lib.draw_grid import draw_grid
from lib.load_setup import load_setup
from res.machines import Conveyor


WIDTH = 1000	# make sure this matches a factor of block_size from function draw_grid! (does right now)
HEIGHT = 400	# make sure this matches a factor of block_size from function draw_grid! (does right now)
BACKGROUND = (255, 255, 255)
MACHINES = list()
LOGISTICS = list()
PRODUCTS = list()
IDS = dict()
MARKED = list()
BUTTONS = list()

class Placeholder():
	"""
	doc
	"""
	size = (25,25)

	def __init__(self, coordinates):
		self.rect = pygame.Rect(coordinates, self.size)
		self.image = pygame.Surface(self.size, flags=pygame.SRCALPHA)
		self.image.fill((255, 204, 153, 110))

class Button():
	"""
	doc
	"""
	def __init__(self, coordinates, size, buttontype):
		self.size = size
		self.rect = pygame.Rect(coordinates, self.size)
		if buttontype == "Run":
			tempimage = pygame.image.load("res/buttons/Button_Run.png").convert()

		self.image = pygame.transform.smoothscale(tempimage, self.size)

def initiate_cursors():
	"""
	doc
	"""
	size = (20,20)
	tempimage = pygame.image.load("res/buttons/glove.png").convert_alpha()
	image_open = pygame.transform.smoothscale(tempimage, size)
	tempimage = pygame.image.load("res/buttons/glove_closed.png").convert_alpha()
	image_closed = pygame.transform.smoothscale(tempimage, size)
	cursor_open = pygame.cursors.Cursor((5,5), image_open)
	cursor_closed = pygame.cursors.Cursor((5,5), image_closed)
	return [cursor_open, cursor_closed]

def main():
	print(manual_mode)
	global MACHINES
	global LOGISTICS
	global PRODUCTS
	global IDS
	clock = pygame.time.Clock()
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))

	if manual_mode is False:
		#TODO: load setup from external file
		IDS, MACHINES, LOGISTICS = load_setup(IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		print("/--- Automatic interface and orientation detection in progress, please wait")
		for j in range(0,len(LOGISTICS)+1):
			for i,entity in enumerate(LOGISTICS):
				if isinstance(entity, Conveyor):
					entity.get_interfaces(LOGISTICS, MACHINES)
					entity.check_orientation(LOGISTICS, MACHINES)	
		print("x/--- Automatic interface and orientation detection in progress, please wait")
		for j in range(0,len(LOGISTICS)+1):
			for i,entity in enumerate(LOGISTICS):
				if isinstance(entity, Conveyor):
					entity.get_interfaces(LOGISTICS, MACHINES)
					entity.check_orientation(LOGISTICS, MACHINES)	
		print("xx/-- Automatic interface and orientation detection in progress, please wait")
		for i, machine in enumerate(MACHINES):
				machine.get_interfaces(LOGISTICS, MACHINES)
				if machine.type == "LidAdder":
					machine.check_orientation(LOGISTICS, MACHINES)
		print("xxx/- Automatic interface and orientation detection in progress, please wait")
		for j in range(0,len(LOGISTICS)+1):
			for i,entity in enumerate(LOGISTICS):
				if isinstance(entity, Conveyor):
					entity.get_interfaces(LOGISTICS, MACHINES)
					entity.check_orientation(LOGISTICS, MACHINES)	
		print("xxxx/ Automatic interface and orientation detection finished")
	else:
		global MARKED
		global BUTTONS
		cursors = initiate_cursors()
		pygame.mouse.set_cursor(cursors[0])
		run_button = Button((925,300), (150,75), "Run")
		BUTTONS.append(run_button)
		mouse_down = False
	SPAWNTIMER, t = pygame.USEREVENT+1, 5000
	pygame.time.set_timer(SPAWNTIMER, t)
	CHECKTIMER, t2 = pygame.USEREVENT+2, 800
	pygame.time.set_timer(CHECKTIMER, t2)
	caption = 'FactorySim'
	pygame.display.set_caption(caption)
	counter = 0
	while 1:
		screen.fill(BACKGROUND)
		draw_grid(screen, HEIGHT, WIDTH, 25)
		#print(pygame.event.get())
		if manual_mode:
			for i,button in enumerate(BUTTONS):
				screen.blit(button.image, button.rect)
			for i,placeholder in enumerate(MARKED):
					screen.blit(placeholder.image, placeholder.rect)
		for event in pygame.event.get():
			if event.type == SPAWNTIMER:
				for j, machine in enumerate(MACHINES):
					PRODUCTS = machine.update(IDS, LOGISTICS, MACHINES, PRODUCTS)
			elif event.type == CHECKTIMER:
				for i, logistic in enumerate(LOGISTICS):
					if logistic.type == "RobotArm":
						logistic.update(PRODUCTS)
		if manual_mode:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					mouse_down = True
				if event.type == pygame.MOUSEBUTTONUP:
					mouse_down = False
			if mouse_down == True:
				pygame.mouse.set_cursor(cursors[1])
				mouse_position = pygame.mouse.get_pos()
				if mouse_position[0] > WIDTH:
					pass # check for pressed buttons
				else:
					temp_x = (int(mouse_position[0]/25 )) *25
					temp_y = (int(mouse_position[1]/25 )) *25
					color_here = screen.get_at((mouse_position[0], mouse_position[1]))
					if color_here == BACKGROUND or color_here == (157,157,157):
						temp_rect = Placeholder((temp_x, temp_y))
						MARKED.append(temp_rect)
					else:
						print(color_here)
					#print(MARKED)
			else:
				pygame.mouse.set_cursor(cursors[0])
		for i,machine in enumerate(MACHINES):
				screen.blit(machine.image, machine.rect)
		if counter == 0:
			for i,entity in enumerate(LOGISTICS):
				screen.blit(entity.image, entity.rect)	
			counter = 1
		else:
			for i,entity in enumerate(LOGISTICS):
				if isinstance(entity, Conveyor):
					screen.blit(entity.image1, entity.rect)	
				else:
					screen.blit(entity.image, entity.rect)
					if entity.type == "RobotArm":
						entity.update(PRODUCTS)
					else:
						entity.update()
			counter = 0		
		for i,product in enumerate(PRODUCTS):
				screen.blit(product.image, product.rect)
				product.update(PRODUCTS, LOGISTICS, MACHINES)

		pygame.display.flip()
		clock.tick(24)
		#slow-mo:
		#clock.tick(5)

if __name__ == "__main__":
	manual_mode = False
	main()