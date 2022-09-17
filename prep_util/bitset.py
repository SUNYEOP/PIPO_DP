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


# setbit0 = lambda k,x: k & ( ~ (1<<x) )
# setbit1 = lambda k,x: k | ( 1 << x )
# setbit = lambda k,x,bit:setbit1(k,x) if bit else setbit0(k,x)

# ithbit = lambda k,i: (k>>i)&1

# delbit = lambda k,i: (upper(k,i+1)<<i) | lower(k,i)

# upper = lambda k,x: k>>x
# lower = lambda k,x: k % (1<<x)
# appendbit0 = lambda k,x: upper(k,x)<<(x+1) | lower(k,x)
# appendbit1 = lambda k,x: setbit1(appendbit0(k,x),x)
# appendbit = lambda k,x,bit:appendbit1(k, x) if bit else appendbit0(k, x)