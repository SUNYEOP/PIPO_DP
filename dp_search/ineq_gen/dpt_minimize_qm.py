import os; import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "prep_util"))

try:
	import sboxes as sb
except Exception as e:
	print("add directorty of mymodule-folder into sys.path")
	raise e

""" Ref : https://pypi.org/project/quine-mccluskey/ 
Version : 0.2"""


from qm import QuineMcCluskey

# Import Target Sboxes
sboxes = [ sb.SBOX_DICTIONARY['PIPOS3'], sb.SBOX_DICTIONARY['PIPOS51'], sb.SBOX_DICTIONARY['PIPOS52'], sb.SBOX_DICTIONARY['PIPO'] ]
names = ["S3K", "S51K", "S52K", "S8K"]
names = dict(zip(sboxes, names))


# Import QM to minimize ineq
qm = QuineMcCluskey()

def dpt_to_zeros(dpt):
	"""
	Note that : order is follow
	LSB ~ MSB of in || LSB ~ MSB of out

	Ex : DPT of S3 [[0], [1, 2, 4], [1, 2, 4], [2, 4], [1, 2, 4], [2, 5], [1, 2], [7]]

	Then return : F^6_2 - {
	0b000000, 
	001001, 001010, 001100, 
	010001, 010010, 010100,
	011010, 011100,
	100001, 100010, 100100,
	101010, 101101,
	110001, 110010,
	111111
	}

	input : dpt

	output : list of (in||out) which can't propagate by dpt.
	"""
	from math import log2; n = int(log2(len(dpt)))
	zeros = []
	num2str = lambda x,n: "".join([str((x>>k)&1) for k in range(n)]) # num to str reverse-order respect to bin()

	for x in range(1<<n):
		i = num2str(x,n)
		for y in range(1<<n):
			if y in dpt[x]:
				continue
			o = num2str(y,n)
			zeros.append( int('0b'+i+o, 2) )
	return zeros

def mini_to_ineqcoef(mini):
	"""
	Note that : order is follow
	1) order of mini
	LSB of in ~ MSB of invar || LSB of out ~ MSB of outvar || constant

	2) order of output
	LSB of in ~ MSB of invar || LSB of out ~ MSB of outvar || constant

	Ex : mini of dpt of S3 
	['-11-01', '1101--', '---011', '--1000', '--01-1', '1-11-0', '1-10-1', '-0-11-', '---110', '0001--', '0--1-1', '1--000', '1110--', '000-1-', '000--1', '-1-000']
	
	Each element of mini is converted into coef like as follow. And return list of coef

	'-11-01' == convert ==> 0 * invar[0] + (1 - invar[1]) + (1 - invar[2]) + 0 * outvar[0] + 1 * outvar[1] + (1 - outvar[2]) >= 1  
	<<<==>>>		 0 * invar[0] - invar[1] - invar[2] + 0 * outvar[0] + 1 * outvar[1] - outvar[2] + 2 >= 0 
	<<<==>>>		 [0, -1, -1, 0, 1, -1, 2] : coef
	

	output : list of coef
	"""
	coefs = []
	for x in mini:
		coef = []
		for y in x:
			if y == '-':
				coef.append(0)
			elif y == '1':
				coef.append(-1)
			else:
				coef.append(1)
		coef.append( coef.count(-1) -1 )
		coefs.append(coef)
	return coefs


file_dir = os.getcwd()
file_name = "sbox_ineq.py"

# For each sbox, make ineq
for sbox in sboxes:
	dpt = sbox.get_DPT()[0]
	ones = dpt_to_zeros(dpt)
	mini = list(qm.simplify(ones)) # make ineq

	ineqmat = mini_to_ineqcoef(mini)

	with open(file_name, 'a') as f:
		f.write(names[sbox] + ' = ' + str(ineqmat) + "\n")

	print(names[sbox] + " : end.")
