import random

def generate_ID(IDS):
		ID = str(random.randint(1,9999))
		while len(ID) < 4:
			ID = "0" + ID
		while ID in IDS.keys():
			ID = str(random.randint(1,9999))
			while len(ID) < 4:
				ID = "0" + ID
		return ID