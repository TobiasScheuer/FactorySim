from res.machines import ProductAdder, StorageUnit, LidAdder, RollerConveyor, TIntersection, RobotArm

def load_setup(IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES):
	"""
	"""
	with open("res/setup_machines.txt", "r") as file:
		lines = file.readlines() # e.g. ProductAdder, 50, 50, horizontal, boxes, /n
		for line in lines:
			content = line.split(',')
			machinetype = content[0]
			coordinates = (int(content[1]), int(content[2]))
			if len(content) == 6:
				orientation = content[3]
				product = content[4]
			else:
				direction = content[3]
			new_machine = None
			if machinetype == "ProductAdder":
				new_machine = ProductAdder(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES, orientation, product)
			elif machinetype == "StorageUnit":
				new_machine = StorageUnit(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
			elif machinetype == "LidAdder":
				new_machine = LidAdder(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
			elif machinetype == "TIntersection":
				new_conveyor = TIntersection(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES, direction)
			elif machinetype == "RobotArm":
				new_conveyor = RobotArm(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES, direction)
			else:
				print(f"Error: Unknown machinetype {machinetype}")
			if new_machine == None:
				LOGISTICS.append(new_conveyor)
				IDS[new_conveyor.ID] = type(new_conveyor)
			else:
				MACHINES.append(new_machine)
				IDS[new_machine.ID] = type(new_machine)
	
	#TODO: Load coordinates etc from setup_machines.txt
	#TODO: Initialize machines in a reading loop
	with open("res/setup_conveyors.txt", "r") as file:
		lines = file.readlines() # e.g. 75,50,/n
		for line in lines:
			content = line.split(',')
			coordinates = (int(content[0]), int(content[1]))
			new_conveyor = RollerConveyor(coordinates, IDS, WIDTH, HEIGHT, LOGISTICS, MACHINES)
			LOGISTICS.append(new_conveyor)
			IDS[new_conveyor.ID] = type(new_conveyor)
		
	return IDS, MACHINES, LOGISTICS