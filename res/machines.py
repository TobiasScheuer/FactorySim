import pygame
from lib.generate_ID import generate_ID
from lib.check_collision import check_collision
import lib.errors as err
from .products import Box, Bottles

class Resources:
	"""
	doc
	"""
	
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		self.check_coordinates(coordinates, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.coordinates = coordinates
		self.ID = generate_ID(IDS)
		self.input_rect = list()		# a list of 25x3 rect  
		self.output_rect = list()		# a list of 25x3 rect  

	def check_coordinates(self, coordinates, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		if coordinates[0] < 0 or coordinates[0] > WIDTH:
			raise err.PlacementError(type(self), coordinates, "horizontal coordinate bounds")
		elif coordinates[1] < 0 or coordinates[1] > HEIGHT:
			raise err.PlacementError(type(self), coordinates, "vertical coordinate bounds")
		for i, entity in enumerate(LOGISTICS+MACHINES):
			if coordinates == entity.coordinates:
				raise err.PlacementError(type(self), coordinates, entity)

	def get_interfaces(self, LOGISTICS, MACHINES):
		"""
		goes through all currently existing machines and logistic elements,
		if one of their output interfaces overlap with own rect -> interface found -> add to own input interfaces
		"""
		combinedlist = MACHINES + LOGISTICS
		for i,logistic in enumerate(combinedlist):
			if logistic.coordinates == self.coordinates:
				if self.ID != logistic.ID:
					print(self.ID)
					print(logistic.ID)
			else:
				outputlist_indexes = self.rect.collidelistall(logistic.output_rect)
				if len(outputlist_indexes) > 0:
					for j in range(0, len(outputlist_indexes)):
						if logistic.output_rect[outputlist_indexes[j]] not in self.input_rect:
							self.input_rect.append(logistic.output_rect[outputlist_indexes[j]])
				inputlist_indexes = self.rect.collidelistall(logistic.input_rect)
				if len(inputlist_indexes) > 0:
					for j in range(0, len(inputlist_indexes)):
						if logistic.input_rect[inputlist_indexes[j]] not in self.output_rect:
							self.output_rect.append(logistic.input_rect[inputlist_indexes[j]])

	def check_orientation(self, LOGISTICS, MACHINES):
		left_interface = pygame.Rect(self.coordinates[0]-1, self.coordinates[1], 3, 25)
		right_interface = pygame.Rect(self.coordinates[0]+24, self.coordinates[1], 3, 25)
		up_interface = pygame.Rect(self.coordinates[0], self.coordinates[1]-1, 25, 3)
		down_interface = pygame.Rect(self.coordinates[0], self.coordinates[1]+24, 25, 3)
		possible_neighbours = [(self.coordinates[0]-25,self.coordinates[1]), (self.coordinates[0]+25,self.coordinates[1]), (self.coordinates[0],self.coordinates[1]+25), (self.coordinates[0],self.coordinates[1]-25)]
		hits = list()
		combinedlist = LOGISTICS+MACHINES
		for i, entity in enumerate(combinedlist):
			if entity.coordinates in possible_neighbours:
				hits.append(entity.coordinates)
		if self.direction == None:
			if isinstance(self, Conveyor):
				if len(hits) > 2 and isinstance(self, RollerConveyor) and isinstance(self, TIntersection) is False: #1D Roller Conveyor supposed to only have 2 neighbors
					raise err.PlacementError(type(self), self.coordinates, "too many neighbours")
				elif len(hits) <= 0:
					pass
				else:
					if len(self.input_rect) == 0:
						if isinstance(self, Conveyor):
							pass
						elif isinstance(self, Machine):
							print("1")
					elif len(self.input_rect) == 1:
						input = self.input_rect[0]
						output_rect = False
						for k in range (0,len(hits)):
							if hits[k][0] < self.coordinates[0]: # neighbour on left flank
								if input.left < self.coordinates[0]: # input on left flank
									pass
								else: # input not on left flank -> has to be output
									output_rect = left_interface
									self.direction = "left"
									self.image = pygame.transform.rotate(self.image, 90)
									self.image1 = pygame.transform.rotate(self.image1, 90)
									break
							elif hits[k][0] > self.coordinates[0]: # neighbour on the right flank
								if input.left > self.coordinates[0]: # input on the right flank
									pass
								else:
									output_rect = right_interface
									self.direction = "right"
									self.image = pygame.transform.rotate(self.image, 270)
									self.image1 = pygame.transform.rotate(self.image1, 270)
									break
							elif hits[k][1] < self.coordinates[1]: # neighbour above
								if input.top < self.coordinates[1]: # input above
									pass
								else:
									output_rect = up_interface
									self.direction = "up"
									#image correct orientation from loading
									break
							elif hits[k][1] > self.coordinates[1]:
								if input.top > self.coordinates[1]:
									pass
								else:
									output_rect = down_interface
									self.direction = "down"
									self.image = pygame.transform.flip(self.image, False, True)
									self.image1 = pygame.transform.flip(self.image1, False, True)
									break
							else:
								print('error3')
						if not output_rect is False:
							if output_rect not in self.output_rect: 
								self.output_rect.append(output_rect)
					elif len(self.input_rect) == 2:
						pass
					elif len(self.input_rect) == 3:
						if isinstance(self, TIntersection):
							possible_interfaces = [left_interface, right_interface, up_interface, down_interface]
							for i in range(0,4):
								if not possible_interfaces[i] in self.input_rect:
									self.output_rect.append(possible_interfaces[i])
									if i == 0:
										self.direction = "left"
										self.image = pygame.transform.rotate(self.image, 90)
										self.image1 = pygame.transform.rotate(self.image1, 90)
									elif i == 1:
										self.direction = "right"
										self.image = pygame.transform.rotate(self.image, 270)
										self.image1 = pygame.transform.rotate(self.image1, 270)
									elif i == 2:
										self.direction = "up"
										#image correct orientation from loading
									else:
										self.direction = "down"
										self.image = pygame.transform.flip(self.image, False, True)
										self.image1 = pygame.transform.flip(self.image1, False, True)
									break
					else:
						print('error1')
						# TODO: create actual error
			elif isinstance(self, Machine):
				if len(self.input_rect) == 0:
					return
				elif len(self.input_rect) == 1:
					input = self.input_rect[0]
				else:
					print(self.input_rect)
					raise err.Other_Error(type(self), self.coordinates)
				if len(hits) != 2:
					raise err.PlacementError(type(self), self.coordinates, "too many neighbours")
				else:	
					output_neighbour = None
					output_rect = None
					for i, hit in enumerate(hits):
						if (hit[0], hit[1]-1) == input.topleft:
							pass
						elif (hit[0], hit[1]+24) == input.topleft:
							pass
						elif (hit[0]-1, hit[1]) == input.topleft:
							pass
						elif (hit[0]+24, hit[1]) == input.topleft:
							pass
						else:
							output_index = i
					output_neighbour = hits[output_index]
					if (output_neighbour[0], output_neighbour[1]) == (self.coordinates[0]+25, self.coordinates[1]):
						output_rect = right_interface
						self.direction = "right"
					elif (output_neighbour[0], output_neighbour[1]) == (self.coordinates[0]-25, self.coordinates[1]):
						output_rect = left_interface
						self.direction = "left"
					elif (output_neighbour[0], output_neighbour[1]) == (self.coordinates[0], self.coordinates[1]+25):
						output_rect = down_interface
						self.direction = "down"
					elif (output_neighbour[0], output_neighbour[1]) == (self.coordinates[0], self.coordinates[1]-25):
						output_rect = up_interface
						self.direction = "up"
					if not output_rect is False:
						if output_rect not in self.output_rect: 
							self.output_rect.append(output_rect)
			else:
				pass
				#print("error4")
		if self.direction == None:
			if len(self.output_rect) == 1:
				output = self.output_rect[0]
				if output == left_interface:	# if only output found, turn conveyor towards output 
					self.direction ="left"
					self.image = pygame.transform.rotate(self.image, 90)
					self.image1 = pygame.transform.rotate(self.image1, 90)
				elif output == right_interface:
					self.direction = "right"
					self.image = pygame.transform.rotate(self.image, 270)
					self.image1 = pygame.transform.rotate(self.image1, 270)
				elif output == up_interface:
					self.direction = "up"
					#image correct orientation from loading
				elif output == down_interface:
					self.direction = "down"
					self.image = pygame.transform.flip(self.image, False, True)
					self.image1 = pygame.transform.flip(self.image1, False, True)
				input_rect = False
				for k in range (0,len(hits)):
					if hits[k][0] < self.coordinates[0]: # neighbour on left flank
						if output.left < self.coordinates[0]: # ouput on left flank
							pass
						else: # output not on left flank -> has to be input
							input_rect = left_interface
					elif hits[k][0] > self.coordinates[0]: # neighbour on the right flank
						if output.left > self.coordinates[0]: # output on the right flank
							pass
						else:
							input_rect = right_interface
					elif hits[k][1] < self.coordinates[1]: # neighbour above
						if output.top < self.coordinates[1]: # output above
							pass
						else:
							input_rect = up_interface
					elif hits[k][1] > self.coordinates[1]: # neighbour below
						if output.top > self.coordinates[1]: # output below
							pass
						else:
							input_rect = down_interface
					else:
						print('error3')
				if not input_rect is False:
					if input_rect not in self.input_rect: 
						self.input_rect.append(input_rect)
			else:
				pass
				#print("error4")

class Machine(Resources):
	"""
	doc
	"""
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		pass

class ProductAdder(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES, orientation, product):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.type = "ProductAdder"
		self.product = product
		if product == "boxes":
			tempimage = pygame.image.load("images/machines/boxAdder.png").convert()
		elif product == "bottles":
			tempimage = pygame.image.load("images/machines/bottleAdder.png").convert()
		else:
			print(f"Error: Setup specified {product} which is an unknown product")
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		self.orientation = orientation
		if orientation == "horizontal":
			output_right = pygame.Rect((coordinates[0]+24, coordinates[1]), (3,25))
			self.output_rect.append(output_right)
			output_left = pygame.Rect((coordinates[0]-3, coordinates[1]), (3,25))
			self.output_rect.append(output_left)
			
		elif orientation == "vertical":
			output_up = pygame.Rect((coordinates[0], coordinates[1]-3), (25,3))
			self.output_rect.append(output_up)
			output_down = pygame.Rect((coordinates[0], coordinates[1]+24), (25,3))
			self.output_rect.append(output_down)

	def update(self, IDS, LOGISTICS, MACHINES, PRODUCTS):
		counter = 0
		for i, logistic in enumerate(LOGISTICS):
			coordinates = (0,0)
			collision = False
			if self.orientation == "horizontal":
				if self.output_rect[0] in logistic.input_rect:	# right output
					coordinates = (self.output_rect[0][0], self.output_rect[0][1] )			
				elif self.output_rect[1] in logistic.input_rect:
					coordinates = (self.output_rect[1][0]-19, self.output_rect[1][1] )
			else:			#vertical
				if self.output_rect[0] in logistic.input_rect:	# top output
					coordinates = (self.output_rect[0][0], self.output_rect[0][1]-19 )			
				elif self.output_rect[1] in logistic.input_rect:
					coordinates = (self.output_rect[1][0], self.output_rect[1][1]-1 )
			if coordinates != (0,0):
				if self.product == "boxes":
					newProduct = Box(coordinates, IDS)
					collision_box = pygame.Rect(coordinates, newProduct.size)
				elif self.product == "bottles":
					newProduct = Bottles(coordinates, IDS)
					collision_box = pygame.Rect(coordinates, newProduct.size)
				collision = check_collision(self.rect, collision_box, PRODUCTS, MACHINES, LOGISTICS, True)
				if collision is False:
					PRODUCTS.append(newProduct)
					counter += 1
				else:
					string = str(type(self)) + " " + self.ID + " overflow!"
					print(string)
			if counter == 2:
				break
		return PRODUCTS
		

class StorageUnit(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.type = "StorageUnit"
		tempimage = pygame.image.load("images/machines/storage.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)
		self.get_interfaces(LOGISTICS, MACHINES)
	
	def update(self, IDS, LOGISTICS, MACHINES, PRODUCTS):
		for i, product in enumerate(PRODUCTS):
			index = product.rect.collidelist(self.input_rect)
			if index > -1:
				new_coordinates = (self.rect[0]+2, self.rect[1]+2)
				product.rect.update(new_coordinates, product.size)
		return PRODUCTS

class LidAdder(Machine):
	"""
	doc
	"""
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.type = "LidAdder"
		tempimage = pygame.image.load("images/machines/box_lid_adder.png").convert_alpha()
		self.image = pygame.transform.smoothscale(tempimage, self.size)
		self.grabbed = False
		self.direction = None
		self.get_interfaces(LOGISTICS, MACHINES)
		self.check_orientation(LOGISTICS, MACHINES)

	
	def update(self, IDS, LOGISTICS, MACHINES, PRODUCTS):
		if self.grabbed is False:
			for i, product in enumerate(PRODUCTS):
				index = product.rect.collidelist(self.input_rect)
				if index > -1:
					new_coordinates = (self.rect[0]+2, self.rect[1]+2)
					product.rect.update(new_coordinates, product.size)
					self.grabbed = True
					break
		else:
			for i,product in enumerate(PRODUCTS):
				index = product.rect.collidelist(self.input_rect)
				if index > -1:
					product.image = product.image_box_lid
					product.lid = True
					if self.output_rect[0].topleft == (self.coordinates[0], self.coordinates[1]-1):
						new_coordinates = (self.coordinates[0]+2, self.coordinates[1]-product.size[1])
					elif self.output_rect[0].topleft == (self.coordinates[0], self.coordinates[1]+24):
						new_coordinates = (self.coordinates[0], self.coordinates[1]+24)
						print("2")
					elif self.output_rect[0].topleft == (self.coordinates[0]-1, self.coordinates[1]):
						new_coordinates = (self.coordinates[0]-5, self.coordinates[1])
						print("3")
					elif self.output_rect[0].topleft == (self.coordinates[0]+24, self.coordinates[1]):
						new_coordinates = (self.coordinates[0]+24, self.coordinates[1])
						print("4")
					else:
						print("error 3249")		
					product.rect.update(new_coordinates, product.size)
					self.grabbed = False
					break
		return PRODUCTS
				
class Logistics(Resources):
	"""
	doc
	"""
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		pass

class Conveyor(Logistics):
	"""
	doc
	"""
	def __init__(self, coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.direction = None	# stores direction of transportation, "up", "down", "left", "right"
		#self.check_orientation(LOGISTICS, MACHINES)
	
	def update(self):
		pass		

class BeltConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		pass
	
	def update(self):
		pass

class RollerConveyor(Conveyor):
	"""
	doc
	"""
	def __init__(self,coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.type = "RollerConveyor"
		tempimage = pygame.image.load("images/machines/rollerConveyor.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		tempimage1 = pygame.image.load("images/machines/rollerConveyor1.png").convert()
		self.image1 = pygame.transform.smoothscale(tempimage1, self.size)	
		self.get_interfaces(LOGISTICS, MACHINES)
		self.check_orientation(LOGISTICS, MACHINES)	# can only be called here since in class __init__ the images are not yet set
			
	
	def update(self):
		pass

class TIntersection(RollerConveyor):
	"""
	2/3 inputs, 1 output, if 2 inputs direction needs to be specified (otherwise type None for automatic orientation)
	"""
	def __init__(self,coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES, direction):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.type = "TIntersection"
		tempimage = pygame.image.load("images/machines/TIntersection.png").convert()
		self.image = pygame.transform.smoothscale(tempimage, self.size)	
		tempimage1 = pygame.image.load("images/machines/TIntersection1.png").convert()
		self.image1 = pygame.transform.smoothscale(tempimage1, self.size)	
		self.direction = direction
		if direction == "up":
			output_interface = pygame.Rect((coordinates[0], coordinates[1]-1), (25,3))
			#picture correct orientation
		elif direction == "down":
			output_interface = pygame.Rect((coordinates[0], coordinates[1]+24), (25,3))
			self.image = pygame.transform.flip(self.image, False, True)
			self.image1 = pygame.transform.flip(self.image1, False, True)
		elif direction == "left":
			output_interface = pygame.Rect((coordinates[0]-1, coordinates[1]), (3,25))
			self.image = pygame.transform.rotate(self.image, 270)
			self.image1 = pygame.transform.rotate(self.image1, 270)
		elif direction == "right":
			output_interface = pygame.Rect((coordinates[0]+24, coordinates[1]), (3,25))
			self.image = pygame.transform.rotate(self.image, 90)
			self.image1 = pygame.transform.rotate(self.image1, 90)
		else:
			print(f"Error: Faulty direction: {direction}")
		if direction != None:
			self.output_rect.append(output_interface)
		self.get_interfaces(LOGISTICS, MACHINES)
		self.check_orientation(LOGISTICS, MACHINES)	# can only be called here since in class __init__ the images are not yet set
		
		
			
	
	def update(self):
		pass

class RobotArm(Logistics):
	"""
	doc
	"""
	def __init__(self,coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES, direction):
		super().__init__(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
		self.grabbed = None
		self.counter = 0
		self.size = (25,25)
		self.rect = pygame.Rect(coordinates, self.size)
		self.type = "RobotArm"
		self.images = dict()
		for i in range(0,8):
			path = "images/machines/robotArm/robotArm" + str(i+1) + ".png"
			tempimage = pygame.image.load(path).convert()
			self.images[i+1] = pygame.transform.smoothscale(tempimage, self.size)		
		self.left_interface = pygame.Rect(self.coordinates[0]-1, self.coordinates[1], 3, 25)
		self.right_interface = pygame.Rect(self.coordinates[0]+24, self.coordinates[1], 3, 25)
		self.up_interface = pygame.Rect(self.coordinates[0], self.coordinates[1]-1, 25, 3)
		self.down_interface = pygame.Rect(self.coordinates[0], self.coordinates[1]+24, 25, 3)
		self.direction = direction
		if direction == "up":
			self.image_index = 1
			self.output_rect.append(self.up_interface)
			self.input_rect = [self.right_interface, self.down_interface, self.left_interface]
		elif direction == "right":
			self.image_index = 3
			self.output_rect.append(self.right_interface)
			self.input_rect = [self.up_interface, self.down_interface, self.left_interface]
		elif direction == "down":
			self.image_index = 5
			self.output_rect.append(self.down_interface)
			self.input_rect = [self.up_interface, self.right_interface, self.left_interface]
		elif direction == "left":
			self.image_index = 7
			self.output_rect.append(self.left_interface)
			self.input_rect = [self.up_interface, self.right_interface, self.down_interface]
		self.image = self.images[self.image_index]
	
	def update(self, PRODUCTS):
		newindex = self.image_index
		new_coordinates = None
		if self.grabbed == None:
			if self.counter < 6:
				self.counter +=1
			else:
				for i, product in enumerate(PRODUCTS):
					if isinstance(product, Bottles):
						index = product.rect.collidelist(self.input_rect)
						if index > -1:
							if self.input_rect[index] == self.left_interface: # left input
								if self.image_index == 7:
									self.grabbed = product.ID
									product.busy = True
								else: 
									newindex = self.find_new_position(7)
							elif self.input_rect[index] == self.right_interface: # right input
								if self.image_index == 3:
									self.grabbed = product.ID
									product.busy = True
								else:
									newindex = self.find_new_position(3)
							elif self.input_rect[index] == self.up_interface: # upper input
								if self.image_index == 1:
									self.grabbed = product.ID
									product.busy = True
								else:
									newindex = self.find_new_position(1)
							elif self.input_rect[index] == self.down_interface: # lower input
								if self.image_index == 5:
									self.grabbed = product.ID
									product.busy = True
								else:
									newindex = self.find_new_position(5)
							self.image_index = newindex
							self.image = self.images[newindex]
							if not self.grabbed == None: 
								new_coordinates = self.moved_product_coordinates()
								product.rect.update(new_coordinates, product.size)
							break
		else: # a product is grabbed
			for i, product in enumerate(PRODUCTS):
				if product.ID == self.grabbed: # find grabbed product
					if isinstance(product, Bottles): 
						for j, product2 in enumerate(PRODUCTS):
							if isinstance(product2, Box) and product2.content == None:
								index = product2.rect.collidelist(self.input_rect)
								if index > -1:
									if self.input_rect[index] == self.left_interface: # left input
										if self.image_index == 7:
											product2.image = product2.image_boxed_bottles
											product2.busy = True
											product2.content = "Bottles"
											self.grabbed = product2.ID
											self.counter = 0
											product.rect.update((-25,-25), product.size)
										else:
											newindex = self.find_new_position(7)
									elif self.input_rect[index] == self.right_interface: # right input
										if self.image_index == 3:
											product2.image = product2.image_boxed_bottles
											product2.busy = True
											product2.content = "Bottles"
											self.grabbed = product2.ID
											self.counter = 0
											product.rect.update((-25,-25), product.size)
										else:
											newindex = self.find_new_position(3)
									elif self.input_rect[index] == self.up_interface: # upper input
										if self.image_index == 1:
											product2.image = product2.image_boxed_bottles
											product2.busy = True
											product2.content = "Bottles"
											self.grabbed = product2.ID
											self.counter = 0
											product.rect.update((-25,-25), product.size)
										else:
											newindex = self.find_new_position(1)
									elif self.input_rect[index] == self.down_interface: # lower input
										if self.image_index == 5:
											product2.image = product2.image_boxed_bottles
											product2.busy = True
											product2.content = "Bottles"
											self.grabbed = product2.ID
											self.counter = 0
											product.rect.update((-25,-25), product.size)
										else:
											newindex = self.find_new_position(5)
									self.image_index = newindex
									self.image = self.images[newindex]		
						if product.ID == self.grabbed: 
							new_coordinates = self.moved_product_coordinates()
							product.rect.update(new_coordinates, product.size)
						break
					elif isinstance(product, Box):
						if self.counter < 30:
							self.counter += 1
						else:
							self.counter = 25
							if self.output_rect[0] == self.left_interface: # left output
								if self.image_index == 7:
									self.grabbed = None
									product.busy = False
									new_coordinates = (self.coordinates[0]-1, self.coordinates[1])
									self.counter = 0
								else:
									newindex = self.find_new_position(7)
							elif self.output_rect[0] == self.right_interface: # right output
								if self.image_index == 3:
									self.grabbed = None
									product.busy = False
									new_coordinates = (self.coordinates[0]+25, self.coordinates[1]+1)
									self.counter = 0
								else:
									newindex = self.find_new_position(3)
							elif self.output_rect[0] == self.up_interface: # upper output
								if self.image_index == 1:
									self.grabbed = None
									product.busy = False
									new_coordinates = (self.coordinates[0]+3, self.coordinates[1]-product.size[1])
									self.counter = 0
								else:
									newindex = self.find_new_position(1)
							elif self.output_rect[0] == self.down_interface: # lower output
								if self.image_index == 5:
									self.grabbed = None
									product.busy = False
									new_coordinates = (self.coordinates[0]+1, self.coordinates[1]+25)
									self.counter = 0
								else:
									newindex = self.find_new_position(5)
							self.image_index = newindex
							self.image = self.images[newindex]	
							if self.grabbed != None:	 
								new_coordinates = self.moved_product_coordinates()
							product.rect.update(new_coordinates, product.size)
							break


	def find_new_position(self, target_position):
		positions = [1,2,3,4,5,6,7,8]       # 1,2,x,4,5,6,7,8                 # 1,2,3,4,5,6,x
		target_index = positions.index(target_position)
		newindex = None
		left_half = positions[0:target_index]
		right_half = positions[target_index+1:]
		while len(left_half) < 4:
			left_half.append(right_half[-1])
			right_half.pop()
		while len(right_half) < 3:
			right_half.append(left_half[0])
			left_half.pop(0)
		if self.image_index == target_position:
			pass
		elif self.image_index in left_half:
			newindex = self.image_index + 1
		elif self.image_index in right_half:
			newindex = self.image_index - 1
		if newindex == 9 or newindex == 0:
			if target_position <= 5:
				newindex = 1
			else:
				newindex = 8
		return newindex

	def moved_product_coordinates(self):
		new_coordinates = (0,0)
		if self.image_index == 1:
			new_coordinates = (self.rect[0]+5, self.rect[1]-10)
		elif self.image_index == 2:
			new_coordinates = (self.rect[0]+10, self.rect[1]-5)
		elif self.image_index == 3:
			new_coordinates = (self.rect[0]+18, self.rect[1]-1)
		elif self.image_index == 4:
			new_coordinates = (self.rect[0]+10, self.rect[1]+5)
		elif self.image_index == 5:
			new_coordinates = (self.rect[0]+5, self.rect[1]+10)
		elif self.image_index == 6:
			new_coordinates = (self.rect[0], self.rect[1]+5)
		elif self.image_index == 7:
			new_coordinates = (self.rect[0]-5, self.rect[1]-1)
		elif self.image_index == 8:
			new_coordinates = (self.rect[0]-10, self.rect[1]-5)
		return new_coordinates

		


