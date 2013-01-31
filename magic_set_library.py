from magic_set import Card
from magic_set import Normal_Mythic_Rare_Set
from magic_set import Normal_Set

class Magic_Set_Library:
	mythic_rare_sets = ['gtc', 'rtr', 'avr', 'nph', 'mbs', 'som', 'roe', 'wwk', 'zen', 'arb', 'con', 'ala', 'm13', 'm12', 'm11', 'm10']
	normal_sets = ['fut']
	
	def __init__(self):
		self.set_map = {}
		for abbreviation in self.mythic_rare_sets:
			rarity_map = self._build_rarity_map('data/'+abbreviation+'_dump.txt')
			self.set_map[abbreviation] = Normal_Mythic_Rare_Set(abbreviation, rarity_map)
		for abbreviation in self.normal_sets:
			rarity_map = self._build_rarity_map('data/'+abbreviation+'_dump.txt')
			self.set_map[abbreviation] = Normal_Set(abbreviation, rarity_map)
	
	def _build_rarity_map(self, file_name):
		rarity_map = {}
		for ln in open(file_name):
			ln_split = ln.strip().split("\t")
			card = Card(ln_split[1], ln_split[4], ln_split[3])
			rarity_map.setdefault(card.rarity, []).append(card)
		return rarity_map
	
	def make_booster(self, magic_set):
		return self.set_map[magic_set].make_booster()