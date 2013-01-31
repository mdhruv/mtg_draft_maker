import random

COLORS = ["Black", "Blue", "Green", "Red", "White"]

class Magic_Set:
	def __init__(self, abbreviation, rarity_map):
		self.abbreviation = abbreviation
		self.rarity_map = rarity_map
	
	def make_booster(self):
		raise NotImplementedError

class Normal_Mythic_Rare_Set(Magic_Set):
	def make_booster(self):
		return_list = []
		while not self._verify(return_list):
			return_list = []
			if random.random() < 0.125:
				return_list.append(random.choice(self.rarity_map['M']))
			else:
				return_list.append(random.choice(self.rarity_map['R']))
			return_list.extend(random.sample(self.rarity_map['U'], 3))
			return_list.extend(random.sample(self.rarity_map['C'], 10))
		return return_list
	
	def _verify(self, booster):
		if not booster:
			return False
		# Lets make sure we have two colors in each booster
		for color in COLORS:
			num_needed = 2
			for card_colors in map(lambda x:x.colors, booster):
				if color in card_colors:
					num_needed-=1
			if num_needed > 0:
				return False
		return True

class Normal_Set(Magic_Set):
	def make_booster(self):
		return_list = []
		while not self._verify(return_list):
			return_list = []
			return_list.append(random.choice(self.rarity_map['R']))
			return_list.extend(random.sample(self.rarity_map['U'], 3))
			return_list.extend(random.sample(self.rarity_map['C'], 10))
		return return_list

	def _verify(self, booster):
		if not booster:
			return False
		# Lets make sure we have two colors in each booster
		for color in COLORS:
			num_needed = 2
			for card_colors in map(lambda x:x.colors, booster):
				if color in card_colors:
					num_needed-=1
			if num_needed > 0:
				return False
		return True
			

class Card:
	def __init__(self, name, rarity, color_str):
		self.name = name
		self.rarity = rarity
		if color_str:
			self.color_str = color_str
		else:
			self.color_str = None
		self.colors = self.convert_color_str(color_str)
	
	def convert_color_str(self, color_str):
		if not color_str:
			return set()
		return set(color_str.split('/'))
	
	def __str__(self):
		return "(%s, %s, %s)" % (self.name, self.rarity, self.color_str)
	
	def __repr__(self):
		return "Card(%s, %s, %s)" % (self.name, self.rarity, self.color_str)
