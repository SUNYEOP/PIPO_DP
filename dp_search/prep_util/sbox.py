from vecbool import *

class Sbox(VecBool):
	"""docstring for Sbox"""
	def __init__(self, LUT):
		super(Sbox, self).__init__(LUT)

	def inverse(self):
		if self.isinv:
			return Sbox(self.invLUT)
		else:
			return None