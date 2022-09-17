# Bit operation
def setbit0(k,x):	return k & ( ~ (1<<x) )
def setbit1(k, x):	return k | ( 1 << x )
def setbit(k,x,bit):
	if bit:
		return setbit1(k,x)
	else:
		return setbit0(k,x)
def ithbit(k, i):	return (k>>i)&1
def upper(k, i):	return k>>i
def lower(k, i):	return k % (1<<i)
def delbit(k, i):	return (upper(k,i+1)<<i) | lower(k,i)
def appendbit0(k, i):	return upper(k,i)<<(i+1) | lower(k,i)
def appendbit1(k, i):	return setbit1(appendbit0(k,x),x)
def appendbit(k, i, bit):
	if bit:
		return appendbit1(k, i)
	else:
		return appendbit0(k, i)

class DP:
	"""docstring for Division_Property"""
	def __init__(self, K, blocksize):
		self.K = K
		self.blocksize_cur = self.blocksize = blocksize

	def show(self):
		print("blocksize : %d"%self.blocksize)
		if self.blocksize != self.blocksize_cur: print("blocksize_cur : %d"%self.blocksize_cur)
		print("K : ", self.K)
	
	def size_reduce(self):
		cnt = 0
		for redundantk in list(self.K):
			for k in self.K:
				if (k != redundantk)&(k&redundantk == k):
					self.K.remove(redundantk)
					cnt += 1
					break
		return cnt

	def copy(self, copyidxs, defaultReduce = True):
		""" The new copied bit based on "copy rule" is appended to the end.
		Ex)
		"""
		if not copyidxs:
			return

		if copyidxs[0]>=self.blocksize_cur:
			raise IndexError("Current block size : %d but, copy index : ("%self.blocksize_cur, copyidxs, ") out of range")

		b, n = self.blocksize_cur, len(copyidxs)

		# Copy rule : 0 -> (0,0) // 1->(1,0), (0,1) 
		for k in list(self.K):
			if ithbit(k,copyidxs[0]): # 1->(1,0), "(0,1) (added)"
				self.K.add( setbit0(setbit1(k,b),copyidxs[0]) )

		self.blocksize_cur += 1

		if defaultReduce:
			self.size_reduce()
		self.copy(copyidxs[1:], defaultReduce = defaultReduce)
		return [(copyidxs[x], b+x) for x in range(n)]

	def xor(self, xorfrom, xorinto, defaultReduce = True):
		if not xorinto:
			return

		n = len(xorfrom)
		if n != len(xorinto):
			raise ValueError("Lengths of xorfrom must equal with lengths xorinto.")
		elif n != len(set(xorfrom)):
			raise ValueError("Xorfrom must not contain duplicates.")

		elif xorfrom[0] in xorinto[1:]:
			raise ValueError("xorinto index %d is xored after it is deleted."%xorfrom[0])

		self.K = set([ delbit( setbit(k, xorinto[0], ithbit(k,xorfrom[0])|ithbit(k,xorinto[0])), xorfrom[0] ) for k in self.K if not 1&(k>>xorfrom[0])&(k>>xorinto[0])])

		if defaultReduce:
			self.size_reduce()

		self.blocksize_cur -= 1
		newxorfrom = [x-1 if x>xorfrom[0] else x for x in xorfrom[1:]]
		newxorinto = [x-1 if x>xorfrom[0] else x for x in xorinto[1:]]
		self.xor(newxorfrom, newxorinto, defaultReduce = defaultReduce)

	def sbox(self, targetidxs, sbox, defaultReduce = True):
		if sbox.inbit != len(targetidxs):
			raise ValueError("Lengths of targetidxs must equal with inbit of Sbox.")

		DPtable = sbox.get_DPT()[0]

		newK = set()
		for k in self.K:
			tablerow = sum([ithbit(k,targetidxs[i])<<i for i in range(len(targetidxs))])
			propaks = DPtable[tablerow]
			addedk = k
			for propak in propaks:
				for i in range(len(targetidxs)):
					addedk = setbit(addedk, targetidxs[i], ithbit(propak, i))
				newK.add(addedk)
		self.K = newK
		if defaultReduce:
			self.size_reduce()

	def bitperm(self, i2permi):
		"""docstring for perm(bit - permutation) : i-th bit ==perm==> perm[i]-th bit """
		if len(i2permi) != self.blocksize_cur:
			raise IndexError("Lengths of permutation must equal to blocksize_cur(%d)"%self.blocksize_cur)
		if set(i2permi) != set([x for x in range(self.blocksize_cur)]):
			raise IndexError("Permutation must have each value only once.")

		else:
			permedk = lambda bp, k: sum([1<<bp[i] for i in range(len(bp)) if ithbit(k, i)])
			self.K = set([permedk(i2permi, k) for k in self.K])




class DPTS(DP):
	"""docstring for DPT(Division Property Three Subset)"""
	def __init__(self, K, L, blocksize):
		super().__init__(K, blocksize)
		self.L = L
		
	def show(self):
		super().show()
		print("L : ", self.L)
		
	def size_reduce(self):
		kcnt = super().size_reduce()
		lcnt = 0
		for l in list(self.L):
			for k in self.K:
				if k&l == k: # l>= k
					self.L.remove(l)
					lcnt += 1
					break
		return kcnt, lcnt

	def copy(self, copyidxs, defaultReduce = True):
		"""
		===== Copy Rule =====
		K 		K'
		0	->	0,0
		1	->	1,0 / 0,1

		L 		L'
		0	->	0,0
		1	->	1,0 / 0,1 / 1,1
		====================
		"""
		if not copyidxs:
			return

		if copyidxs[0]>=self.blocksize_cur:
			raise IndexError("Current block size : %d but, copy index : ("%self.blocksize_cur, copyidxs, ") out of range")

		b, n = self.blocksize_cur, len(copyidxs)

		for k in list(self.K):
			if ithbit(k,copyidxs[0]): # 1->(1,0), "(0,1) (added)"
				self.K.add( setbit0(setbit1(k,b),copyidxs[0]) )

		for l in list(self.L):
			if ithbit(l,copyidxs[0]):
				self.L.add( setbit1(l, b) ) # 1->(1,0), (0,1), "(1,1)""
				self.L.add( setbit0( setbit1(l,b), copyidxs[0]) ) # 1->(1,0), "(0,1)", (1,1) 

		self.blocksize_cur += 1

		if defaultReduce:
			self.size_reduce()
		self.copy(copyidxs[1:], defaultReduce = defaultReduce)
		return [(copyidxs[x], b+x) for x in range(n)]

	def xor(self, xorfrom, xorinto, defaultReduce = True):
		"""
		===== XOR Rule =====
		K 					K'
		0,0		----->		0
		1,0/0,1	----->		1
							
		L	 				L'
		0,0		-xor->		0
		1,0/0,1	-xor->		1
		====================
		"""		
		if not xorinto:
			return

		n = len(xorfrom)
		if n != len(xorinto):
			raise ValueError("Lengths of xorfrom must equal with lengths xorinto.")
		elif n != len(set(xorfrom)):
			raise ValueError("Xorfrom must not contain duplicates.")
		elif xorfrom[0] in xorinto[1:]:
			raise ValueError("xorinto index %d is xored after it is deleted."%xorfrom[0])

		# only if k1 + k2 <= 1
		self.K = set([ delbit( setbit(k, xorinto[0], ithbit(k,xorfrom[0])|ithbit(k,xorinto[0])), xorfrom[0] ) for k in self.K if not 1&(k>>xorfrom[0])&(k>>xorinto[0])])

		# "Lprime <=xor= lprime" means Lprime = symmetric_difference( Lprime, {lprime} )
		newL = set()
		for l in self.L:
			lsum = 1&(l>>xorfrom[0])&(l>>xorinto[0])
			if not lsum: # only if l1 + l2 <= 1
				lprime = delbit(setbit(l, xorinto[0], lsum), xorfrom[0])
				newL.symmetric_difference_update([lprime])
		self.L = newL

		if defaultReduce:
			self.size_reduce()

		self.blocksize_cur -= 1
		newxorfrom = [x-1 if x>xorfrom[0] else x for x in xorfrom[1:]]
		newxorinto = [x-1 if x>xorfrom[0] else x for x in xorinto[1:]]
		self.xor(newxorfrom, newxorinto, defaultReduce = defaultReduce)

	def sbox(self, targetidxs, sbox, defaultReduce = True):
		super().sbox(targetidxs, sbox, defaultReduce = False)

		DPtable = sbox.get_DPT()[1]

		newL = set()
		for l in self.L:
			tablerow = sum([ithbit(l, targetidxs[i])<<i for i in range(len(targetidxs))])
			propals = DPtable[tablerow]
			addedl = l
			for propal in propals:
				# change bit of l into bit of propagated l
				for i in range(len(targetidxs)):
					addedl = setbit(addedl, targetidxs[i], ithbit(propal, i))
				newL.add(addedl)
		self.L = newL
		if defaultReduce:
			self.size_reduce()

	def bitperm(self, i2permi):
		"""docstring for perm(bit - permutation) : i-th bit ==perm==> perm[i]-th bit """
		super().bitperm(i2permi)

		permedl = lambda bp, l: sum([1<<bp[i] for i in range(len(bp)) if ithbit(l, i)])
		self.L = set([permedl(i2permi, l) for l in self.L])

	def keyxor(self, keyxoridxs, defaultReduce = True):
		"""
		===== Key-XOR Rule =====
		Assuming a round key is Xored with the i-th bit.
		K' U= {(ln-1, ln-2, ... , li+1, 1, li-1, ... , l0)} for all l in L s.t. li = 0
		L' == L
		========================
		"""		
		if not keyxoridxs:
			return

		if self.blocksize_cur < len(keyxoridxs):
			raise ValueError("Lengths of keyxoridxs(%d) must be smaller(or equal) than blocksize(%d)."%(len(keyxoridxs), self.blocksize_cur))
		elif max(keyxoridxs) >= self.blocksize_cur:
			raise IndexError("Key xor idx(%d) must be smaller than blocksize(%d)"%(max(keyxoridxs), self.blocksize_cur))

		for l in self.L:
			self.K |= set([setbit1(l,idx) for idx in keyxoridxs if ithbit(l,idx) == 0])

		if defaultReduce:
			self.size_reduce()

	def constxor(self, constidxs, defaultReduce = True):
		"""
		===== 1-XOR Rule =====
		Assuming "1" is Xored with the i-th bit.
		K' = K
		L' == L XOR { {(ln-1, ln-2, ... , li+1, 1, li-1, ... , l0)} } for all l in L s.t. li = 0.
		Note that, redundant vector can be generated. So, do Reduce.
		========================
		"""
		if not constidxs:
			return

		if self.blocksize_cur < len(constidxs):
			raise ValueError("Lengths of constidxs(%d) must be smaller(or equal) than blocksize(%d)."%(len(constidxs), self.blocksize_cur))
		elif max(constidxs) >= self.blocksize_cur:
			raise IndexError("Constant(= 1) xor idx(%d) must be smaller than blocksize(%d)"%(max(constidxs), self.blocksize_cur))

		for idx in constidxs:
			self.L.symmetric_difference_update([setbit1(l, idx) for l in self.L if ithbit(l, idx) == 0])

		if defaultReduce:
			self.size_reduce()