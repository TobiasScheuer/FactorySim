import pygame
from lib.generate_ID import generate_ID
from lib.check_collision import check_collision

class Product:
	"""
	doc
	"""
	def __init__(self, coordinates, IDS):
		"""
		doc
		"""
		self.ID = generate_ID(IDS)
		self.busy = False
	
	def update(self, PRODUCTS, LOGISTICS, MACHINES):
		"""
		doc
		"""
		if self.busy is False:
			upc = 0
			downc = 0
			leftc = 0
			rightc = 0
			xcenter = self.rect[0] + int(self.size[0]*0.5)
			ycenter = self.rect[1] + int(self.size[1]*0.5)
			xline = ((self.rect[0], ycenter ) , ( self.rect[0] + self.size[0],  ycenter))
			yline = ((xcenter, self.rect[1] ) , ( xcenter, self.rect[1]+self.size[1]))
			collision = False
			for i, logistic in enumerate(LOGISTICS):
				if logistic.direction == "up" or logistic.direction == "down":
					yclip = logistic.rect.clipline(yline) #yclip containts line part coordinates which is in logistic rect
					if yclip:	# evaluates if yclip has contents and there is inside the 
						if logistic.direction == "up":
							if upc == 0:
								collision_box = pygame.Rect(self.rect[0], self.rect[1]-1, self.size[0], self.size[1]+1)
								collision = check_collision(self.rect, collision_box, PRODUCTS, MACHINES, LOGISTICS)
								if collision is False:
									self.rect = self.rect.move(0,-1)
								upc += 1
						elif logistic.direction == "down":
							if downc == 0:
								collision_box = pygame.Rect(self.rect[0], self.rect[1], self.size[0], self.size[1]+1)
								collision = check_collision(self.rect, collision_box, PRODUCTS, MACHINES, LOGISTICS)
								if collision is False:
									self.rect = self.rect.move(0,1)
								downc += 1
				else:   # direction == left or right
					xclip = logistic.rect.clipline(xline) #yclip containts line part coordinates which is in logistic rect
					if xclip:	# evaluates if yclip has contents and there is inside the 
						if logistic.direction == "left":
							if leftc == 0:
								collision_box = pygame.Rect(self.rect[0]-1, self.rect[1], self.size[0]+1, self.size[1])
								collision = check_collision(self.rect, collision_box, PRODUCTS, MACHINES, LOGISTICS)
								if collision is False:
									self.rect = self.rect.move(-1,0)
								leftc += 1
						elif logistic.direction == "right":
							if rightc == 0:
								collision_box = pygame.Rect(self.rect[0], self.rect[1], self.size[0]+1, self.size[1])
								collision = check_collision(self.rect, collision_box, PRODUCTS, MACHINES, LOGISTICS) 
								if collision is False:
									self.rect = self.rect.move(1,0)
								rightc += 1
			machine_index = self.rect.collidelist(MACHINES)
			if machine_index >= 0:
				machine = MACHINES[machine_index]
				if isinstance(machine, StorageUnit):
					self.rect.update((machine.coordinates[0]+3, machine.coordinates[1]+3), self.size)
					self.busy = True

class Box(Product):
	"""
	doc
	"""
	size = (19,17)

	def __init__(self, coordinates, IDS):
		super().__init__(coordinates, IDS)
		
		self.rect = pygame.Rect((coordinates[0]+3, coordinates[1]+3), self.size)
		tempimage = pygame.image.load("images/products/box.png").convert_alpha()
		self.image_empty = pygame.transform.smoothscale(tempimage, self.size)	
		tempimage = pygame.image.load("images/products/boxedBottles.png").convert_alpha()
		self.image_boxed_bottles = pygame.transform.smoothscale(tempimage, self.size)
		tempimage = pygame.image.load("images/products/box_lid.png").convert_alpha()
		self.image_box_lid = pygame.transform.smoothscale(tempimage, self.size)
		self.image = self.image_empty
		self.content = None 
		self.lid = False

class Bottles(Product):
	"""
	doc
	"""
	size = (19,17)
	
	def __init__(self, coordinates, IDS):
		super().__init__(coordinates, IDS)
		self.rect = pygame.Rect((coordinates[0]+3, coordinates[1]+3), self.size)
		tempimage = pygame.image.load("images/products/bottles.png").convert_alpha()
		self.image = pygame.transform.smoothscale(tempimage, self.size)
		
		

