from boolean import *
from bitset import *

log2 = lambda x: 0 if x==1 else 1+log2(x>>1) # Return integer part of log_2(x)

def LUT_to_TFT_v(LUT, outbit = None):
	"""
	Parameters:													Returns:
	-----------													--------	
	LUT:		Look up table of Sbox // list of integer		TFT_v:		vector of Truth-False Table(bit-wise) of coordinate LUT
	outbit: 	if Sbox is not n-bit to n-bit Sbox 

	Parameter Usage or Example:
	-----------
	3 bit LUT S3 of PIPO
	S3 = [4, 7, 5, 0, 3, 2, 1, 6]

			  --0---1---2----
	S3[7]=6	  |	0	1	1	|
	S3[6]=1	  |	1	0	0	|
	S3[5]=2	  |	0	1	0	|			==>		Output	=	[i-th column value]
	S3[4]=3	  |	1	1	0	|							=	[0b 01010110 ,0b 10110010, 0b 10000111]
	S3[3]=0	  |	0	0	0	|								
	S3[2]=5	  |	1	0	1	|								
	S3[1]=7	  |	1	1	1	|
	S3[0]=4	  |	0	0	1	|
 			  ----------------
	"""
	n = log2(len(LUT)) if not outbit else outbit
	mask = [1<<x for x in range(n)]

	TFT_v = [0 for x in range(n)]
	for value in reversed(LUT):
		for i in range(n):
			TFT_v[i] <<=1
			if value&mask[i]:
				TFT_v[i] +=1
	return TFT_v

def reduceBitset(K, num_elements):
	"""
	Description:
	------------
	Delete redundant vectors(i.e. not minimal vectors)
	k' is redundant means exist k s.t. k'> k (i.e. k'&k == k')

	Parameters:											 			Returns:
	-----------											 			--------
	K:			Bit Set									 			newK:		Bit Set. redundant elements are removed							

	Parameter Usage or Example:
	-----------
	Case: K = 0b 1010 0000 (i.e. == {5, 7}), size = 3
	Notethat : 7(0b 111) > 5(0b 101). --> 7 is redundant
	So, 7 is removed and return 0b 0010 0000
	"""
	newK = K
	num_bit = log2(num_elements)
	for u in range(num_elements):
		if ithbit(newK,u):
			zerobits = [1<<x for x in range(num_bit) if (u>>x)&1 == 0]
			succ = [u + sum([zerobits[x] for x in range(len(zerobits)) if ithbit(idx,x)]) for idx in range(1,1<<len(zerobits))]		# list of elements exceeding than u
			for x in succ:
				newK = setbit0(newK, x)
				# newK = setbit(newK, x, 0)
	return newK

class VecBool():
	"""docstring for VecBool
	Vectorial Boolean Function is equivalent to Sbox.
	But in our case, we are dealing with a more algebraic part."""
	class_attr = ["LUT", "n", "coordinate", "DPTK", "DPTL"]
	class_method = ["component(u)", "product(u)", "degree", "mindegree"]
	future_attr = []
	def __init__(self, LUT, defaultoutbit = None):
		if (1<<log2(len(LUT))) != len(LUT):
			raise ValueError("LUT size must be 2**n.")
		# super(Sbox, self).__init__()
		self.LUT 			= tuple(LUT)
		self.n = self.inbit	= log2(len(LUT))

		for x in range(len(LUT)):
			if not x in LUT:
				self.isinv	= False
				break
		else:
			self.isinv		= True

		if self.isinv:
			self.invLUT		= tuple([LUT.index(x) for x in range(1<<self.n)])
			self.outbit		= self.inbit
		else:
			self.invLUT 	= None
			if defaultoutbit:
				self.outbit = defaultoutbit
			else:
				self.outbit = log2(max(LUT)) + 1
		self.coordinate		= [Boolean(TFT,self.inbit) for TFT in LUT_to_TFT_v(LUT, self.outbit)]

	def show(self):
		print("%d-bit to %d-bit Vectorial Boolean Function with LUT as follow.\n"%(self.inbit, self.outbit), self.LUT)

	def inverseVecBool(self):
		if self.isinv:
			return VecBool(self.invLUT)
		else:
			return None

	def component(self, u):
		if u == 0:
			return ConstantBool(self.inbit, 1)		# constant(1) boolean function

		TFT_comp = 0
		for i in range(self.outbit):
			if ithbit(u,i):
				TFT_comp ^= self.coordinate[i].TFT
		return Boolean(TFT_comp, self.inbit)

	def get_degree(self):
		if "degree" in dir(self):
			return self.degree

		# degs = self.degrees = [i.get_degree for i in self.coordinate]
		degs = [i.get_degree() for i in self.coordinate]
		self.degree = max(degs)
		return self.degree

	def get_mindeg(self):
		if "mindeg" in dir(self):
			return self.mindeg

		# col : 1<<inbit, row : outbit

		ANFv = [x.ANF for x in self.coordinate]
		sortedidx = sorted( [(x, bin(x).count("1")) for x in range(1<<self.inbit)], key = lambda k:k[-1], reverse = True )

		rank = 0
		for col in range(1<<self.inbit):
			for pivotrow in range(rank, self.outbit):
				if ithbit(ANFv[pivotrow], sortedidx[col][0]): # Find pivot row
					ANFv[rank], ANFv[pivotrow] = ANFv[pivotrow], ANFv[rank]	# Swap row

					# reducing below rows
					for row in range(pivotrow + 1, self.outbit):
						if ithbit(ANFv[row], sortedidx[col][0]):
							ANFv[row] ^= ANFv[rank]

					rank += 1
					break						

			if rank == self.outbit:
				mindeg = sortedidx[col][1]
				break
		else:	# If not full rank
			mindeg = 0

		self.mindeg = mindeg
		return mindeg

	def product(self, u):
		if u == 0:
			return ConstantBool(self.inbit, 1)		# constant(1) boolean function
		TFT_product = -1
		for i in range(self.outbit):
			if ithbit(u,i):
				TFT_product &= self.coordinate[i].TFT
		return Boolean(TFT_product, self.inbit)

	def get_DPT(self):
		""" Docstring for gdt_DPT
		Note that : order is follow
		MSB ~ LSB of integer
		"""
		if "DPTK" in dir(self):												# If object already has attributes "DPTK", "DPTL"
			return self.DPTK, self.DPTL

		DPTK, DPTL = [0 for x in range(1<<self.inbit)], [0 for x in range(1<<self.inbit)]
		for u in range(1<<self.outbit):
			productfunc = self.product(u)									# Compute f^u
			for monomial in productfunc.get_monomials():					# for each monomials in productfunction
				# DPTL[monomial] = setbit(DPTL[monomial], u, 1)				# if sum of monomial is 1, then f^u become 1 based on input div K, L == empty, {monomial}
				DPTL[monomial] = setbit1(DPTL[monomial], u)					# if sum of monomial is 1, then f^u become 1 based on input div K, L == empty, {monomial}

				# make submonomial step
				# if monomial : 0b1101( x3x2x0 ), then onebitidx : [0, 2, 3] and submonomials : ['0b0'(1), '0b1'(x0), '0b100'(x2), '0b101'(x2x0), '0b1000'(x3), '0b1001'(x3x0), '0b1100'(x3x2), '0b1101'(x3x2x0)]
				onebitidx = [x for x in range(self.inbit) if ithbit(monomial,x)]
				submonomials = [sum([1<<onebitidx[x] for x in range(len(onebitidx)) if ithbit(idx,x)]) for idx in range(1<<len(onebitidx))]
				for submonomial in submonomials:
					# DPTK[submonomial] = setbit(DPTK[submonomial],u, 1)		# if submonomial is in unknown set, then f^u become unknown. So DPTK[submonomial] U= u
					DPTK[submonomial] = setbit1(DPTK[submonomial],u)		# if submonomial is in unknown set, then f^u become unknown. So DPTK[submonomial] U= u

		DPTK = [reduceBitset(x,1<<self.n) for x in DPTK];
		self.DPTK = [[monomial for monomial in range(1<<self.inbit) if ithbit(bitsetK,monomial)] for bitsetK in DPTK]
		self.DPTL = [[monomial for monomial in range(1<<self.inbit) if ithbit(bitsetK,monomial)] for bitsetK in DPTL]
		return self.DPTK, self.DPTL

# s = [
# 0x5e, 0xf9, 0xfc, 0x0, 0x3f, 0x85, 0xba, 0x5b, 0x18, 0x37, 0xb2, 0xc6, 0x71, 0xc3, 0x74, 0x9d,
# 0xa7, 0x94, 0xd, 0xe1, 0xca, 0x68, 0x53, 0x2e, 0x49, 0x62, 0xeb, 0x97, 0xa4, 0xe, 0x2d, 0xd0,
# 0x16, 0x25, 0xac, 0x48, 0x63, 0xd1, 0xea, 0x8f, 0xf7, 0x40, 0x45, 0xb1, 0x9e, 0x34, 0x1b, 0xf2,
# 0xb9, 0x86, 0x3, 0x7f, 0xd8, 0x7a, 0xdd, 0x3c, 0xe0, 0xcb, 0x52, 0x26, 0x15, 0xaf, 0x8c, 0x69,
# 0xc2, 0x75, 0x70, 0x1c, 0x33, 0x99, 0xb6, 0xc7, 0x4, 0x3b, 0xbe, 0x5a, 0xfd, 0x5f, 0xf8, 0x81,
# 0x93, 0xa0, 0x29, 0x4d, 0x66, 0xd4, 0xef, 0xa, 0xe5, 0xce, 0x57, 0xa3, 0x90, 0x2a, 0x9, 0x6c,
# 0x22, 0x11, 0x88, 0xe4, 0xcf, 0x6d, 0x56, 0xab, 0x7b, 0xdc, 0xd9, 0xbd, 0x82, 0x38, 0x7, 0x7e,
# 0xb5, 0x9a, 0x1f, 0xf3, 0x44, 0xf6, 0x41, 0x30, 0x4c, 0x67, 0xee, 0x12, 0x21, 0x8b, 0xa8, 0xd5,
# 0x55, 0x6e, 0xe7, 0xb, 0x28, 0x92, 0xa1, 0xcc, 0x2b, 0x8, 0x91, 0xed, 0xd6, 0x64, 0x4f, 0xa2,
# 0xbc, 0x83, 0x6, 0xfa, 0x5d, 0xff, 0x58, 0x39, 0x72, 0xc5, 0xc0, 0xb4, 0x9b, 0x31, 0x1e, 0x77,
# 0x1, 0x3e, 0xbb, 0xdf, 0x78, 0xda, 0x7d, 0x84, 0x50, 0x6b, 0xe2, 0x8e, 0xad, 0x17, 0x24, 0xc9,
# 0xae, 0x8d, 0x14, 0xe8, 0xd3, 0x61, 0x4a, 0x27, 0x47, 0xf0, 0xf5, 0x19, 0x36, 0x9c, 0xb3, 0x42,
# 0x1d, 0x32, 0xb7, 0x43, 0xf4, 0x46, 0xf1, 0x98, 0xec, 0xd7, 0x4e, 0xaa, 0x89, 0x23, 0x10, 0x65,
# 0x8a, 0xa9, 0x20, 0x54, 0x6f, 0xcd, 0xe6, 0x13, 0xdb, 0x7c, 0x79, 0x5, 0x3a, 0x80, 0xbf, 0xde,
# 0xe9, 0xd2, 0x4b, 0x2f, 0xc, 0xa6, 0x95, 0x60, 0xf, 0x2c, 0xa5, 0x51, 0x6a, 0xc8, 0xe3, 0x96,
# 0xb0, 0x9f, 0x1a, 0x76, 0xc1, 0x73, 0xc4, 0x35, 0xfe, 0x59, 0x5c, 0xb8, 0x87, 0x3d, 0x2, 0xfb]
# s = VecBool(s)


# print(s.get_DPT()[0][3])
# for x in range(10):
# 	if x == 10:
# 		print("ok",x)
# 		break
# else:
# 	print("no")

# t = s.product(8).ANF_str(isprint = True)
# print("x1x0" in t)