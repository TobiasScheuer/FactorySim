from pygame import rect

def check_collision(own_rect, collision_box, PRODUCTS, MACHINES, LOGISTICS, ignore_machines=False):
	"""
	method to check if a moved or spawned product would collide with another product or machine
	IN:
		own_rect: pygame.Rect box representing the current location of a product
		collision_box: pygame.Rect box representing the area where a product wants to move to
		PRODUCTS: List of products
		MACHINES: List of machines
		LOGISTICS: List of logistics
		(OPT)ignore_machines: flag if collisions with machines should be ignored (Default:False)
	DO:
		checks for rect overlap with all other products and machines
	OUT:
		returns True for a detected collision and False if not
	"""
	collision = False
	for i, product in enumerate(PRODUCTS):
		if product.rect.colliderect(collision_box) is True and not product.rect == own_rect:
			collision = True
			break
	if ignore_machines is False:
		for j, machine in enumerate(MACHINES):
			if machine.rect.colliderect(collision_box) is True:
				collision = True
				break
		for k, logistic in enumerate(LOGISTICS):
			if logistic.type == "RobotArm": 
				if logistic.rect.colliderect(collision_box) is True:
					collision = True
					break
	return collision