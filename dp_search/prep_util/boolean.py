ithbit = lambda k, i: (k>>i)&1
log2 = lambda x: 0 if x==1 else 1+log2(x>>1) # Return integer part of log_2(x)

def ANFT(TFT, n_bit):
	"""
	Algebraic Normal Form Transformation

	Function to transform Truth-False Table(TFT) to Algebraic-Normal Form Table(AFT)

	Parameters:
	-----------
	TFT:		Bit-wise Truth-False Table
	n_bit:		the number of input bits of boolean function coresponding TFT

	Returns:
	--------
	ANF:		Bit-wise ANF-table of TFT

	Parameter Usage or Example:
	-----------
	TFT of 0-th coordinate function of PIPO Sbox S3
	
	input : 0b 01010110			Output ANF = 0b 01010110
	----x0	x1	x2---------		idx	|	monomial	|	coefficient
	TFT[1	1	1]	=	0 |		7	|	x2x1x0		|	0	T[0] + T[1] + T[2] + T[3] + T[4] + T[5] + T[6] + T[7]
	TFT[0	1	1]	=	1 |		6	|	x2x1 		|	1	T[0] + T[2] + T[4] + T[6]
	TFT[1	0	1]	=	0 |		5	|	x2x0 		|	0	T[0] + T[1] + T[4] + T[5]
	TFT[0	0	1]	=	1 |		4	|	x2 			|	1	T[0] + T[4]
	TFT[1	1	0]	=	0 |		3	|	x1x0 		|	0	T[0] + T[1] + T[2] + T[3]
	TFT[0	1	0]	=	1 |		2	|	x1 			|	1	T[0] + T[2]
	TFT[1	0	0]	=	1 |		1	|	x0 			|	1	T[0] + T[1]
	TFT[0	0	0]	=	0 |		0	|	1 			|	0	T[0]
	--------------------------------------------------------------------------------------------
	"""
	mask = [0x5555555555555555, 0x3333333333333333, 0x0F0F0F0F0F0F0F0F, 0x00FF00FF00FF00FF, 0x0000FFFF0000FFFF, 0x00000000FFFFFFFF]

	if n_bit > 6: 		# mask size up
		for x in range(6,n_bit):
			mask = [ ( k << (1<<x) ) | k for k in mask]
			mask.append( ( 1 << (1<<x) ) - 1 )

	ANF = TFT
	for i in range(n_bit):
		ANF ^= ( (ANF&mask[i]) << (1<<i) )
	return ANF

def monomial_expression(monomial, n, var = 'x'):
	if monomial == 0:
		return "1"
	else:
		outstr = ""
		for x in reversed(range(n)):
			if ithbit(monomial, x):
				outstr += var + str(x)
		return outstr

class Boolean():
	"""docstring for Boolean"""
	class_attr 		= ["TFT", "n", "ANF"]
	class_method 	= ["get_degree", "ANF_str"]
	def __init__(self, TFT, n):
		if len(bin(TFT)[2:]) > (1<<n):
			raise ValueError("TFT size must be less(or equal) than 2**%d."%n)
		self.TFT 	= TFT
		self.n 		= n
		self.ANF 	= ANFT(TFT, n)
	
	def get_monomials(self):
		return [x for x in range(1<<self.n) if ithbit(self.ANF, x)]

	def get_degree(self):
		if "degree" in dir(self):
			return self.degree
		else:
			monomials = self.get_monomials()
			if not monomials:
				self.degree = 0
				return 0
			else:
				self.degree = max([bin(monomial).count("1") for monomial in self.get_monomials()])
				return self.degree

	def ANF_str(self, isprint = False, var = 'x'):
		monomials = self.get_monomials()
		if not monomials:
			print("0")
			return "0"
		else:
			outstr = ""
			for monomial in reversed(monomials):
				outstr += monomial_expression(monomial, self.n, var = var) + "+"
			if isprint:
				print(outstr[:-1])
			return outstr[:-1]

def ConstantBool(n, constant):
	if not constant in [0,1]:
		raise ValueError("Constant in ConstantBool must be 0 or 1.")
	elif constant:	# if constant bit == 1
		return Boolean((1 << (1 << n)) - 1, n)
	else:
		return Boolean(0, n)