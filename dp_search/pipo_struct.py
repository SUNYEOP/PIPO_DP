import numpy as np; import gurobipy as gp; from gurobipy import GRB; import os; import sys
try:
	from sbox_ineq import S3K, S51K, S52K, S8K  # S3K, S51K, S52K, S8K
except Exception as e:
	print("Add directory of ineq folder into system path\n")
	raise e

ineqs = dict([('S3K', np.matrix(S3K)), ("S51K", np.matrix(S51K)), ("S52K", np.matrix(S52K)), ("S8K", np.matrix(S8K))])

# i-th bit == R-layer ==> BP[i]-th bit
# Note that the column index is reversed as the paper describes.
BP=	[  	0,  1,  2,  3,  4,  5,  6,  7, #<<< 0
       15,  8,  9, 10, 11, 12, 13, 14, #<<< 7
       20, 21, 22, 23, 16, 17, 18, 19, #<<< 4
       27, 28, 29, 30, 31, 24, 25, 26, #<<< 3
       38, 39, 32, 33, 34, 35, 36, 37, #<<< 6
       45, 46, 47, 40, 41, 42, 43, 44, #<<< 5
       49, 50, 51, 52, 53, 54, 55, 48, #<<< 1
       58, 59, 60, 61, 62, 63, 56, 57] #<<< 2
blocksize = 64
sboxsize = 8

# add linear constraints for Sbox to model
def sboxConstr(model , inVar , outVar, ineqmat, constrname = None):
	"""
	model		: Gurobi model object
	inVar		: Gurobi Variables with shape = (n1,)
	outVar		: Gurobi Variables with shape = (n2,)
	ineqmat		: numpy matrix with shape = (m, n1 + n2 + 1) where m is the number of linear constraints
	Note that	: order of element of ineqmat == LSB of invar ~ MSB of invar || LSB of outvar ~ MSB of outvar || constant
	-----
	Ex)
	"linear constraints"
	-2 * inVar[0] + -1 * inVar[1] + -1 * inVar[2] + 0 * outVar[0] + 1 * outVar[1] + 1 * outVar[2] + 2 >= 0
	-1 * inVar[0] +  0 * inVar[1] +  0 * inVar[2] + 0 * outVar[0] + 0 * outVar[1] + 0 * outVar[2] + 1 >= 0
	
	"ineqmat"
	np.matrix([[-2, -1, -1, 0, 1, 1, 2], [-1, 0, 0, 0, 0, 0, 1]])
	"""
	if 1 != len(inVar.shape): raise InputError("inVar.shape must be 1-d array")
	elif 1 != len(outVar.shape): raise InputError("outVar.shape must be 1-d array")
	elif 2 != len(ineqmat.shape) : raise InputError("ineqmat.shape must be 2-d array")
	elif (inVar.shape[0] + outVar.shape[0] + 1) != ineqmat.shape[1]: raise IndexError("ineqmat's col size is %d but it is not equal of inVar.shape[0](%d) + outVar.shape[0](%d) + 1"%(ineqmat.shape[1], inVar.shape[0], outVar.shape[0]))
	n = inVar.shape[0]
	m = outVar.shape[0]
	if constrname:
		model.addConstr(ineqmat[:,:n] @ inVar + ineqmat[:,n:n+m] @ outVar + np.array(ineqmat[:,-1]).reshape(-1) >= 0, name = constrname)
	else:
		model.addConstr(ineqmat[:,:n] @ inVar + ineqmat[:,n:n+m] @ outVar + np.array(ineqmat[:,-1]).reshape(-1) >= 0)

def piposboxConstr(model , inVar , outVar, rounds, col):
	# S3
	outS3 = model.addMVar(shape = 3, vtype = GRB.BINARY, name 					= "(%d,%d)/outS3"%(rounds,col))
	sboxConstr(model, inVar[:3], outS3, ineqs["S3K"], constrname				= "(%d,%d)/S3"%(rounds,col))
	#inVar[:3] --S3-> outS3

	# S5_1
	outS51 = model.addMVar(shape = 5, vtype = GRB.BINARY, name 					= "(%d,%d)/outS51"%(rounds,col))
	sboxConstr(model, inVar[3:], outS51, ineqs['S51K'], constrname				= "(%d,%d)/S51"%(rounds,col))
	#inVar[3:] --S51-> outS51

	# Copy output 3-bit of S3
	outS3c1 = model.addMVar(shape = 3, vtype = GRB.BINARY, name					= "(%d,%d)/outS3-c1"%(rounds,col))
	outS3c2 = model.addMVar(shape = 3, vtype = GRB.BINARY, name					= "(%d,%d)/outS3-c2"%(rounds,col))
	model.addConstr( outS3 == outS3c1 + outS3c2, name 							= "(%d,%d)/copyS3"%(rounds,col))
	# XOR1
	outxor1 = model.addMVar(shape = 3, vtype = GRB.BINARY, name				    = "(%d,%d)/outxor1"%(rounds,col))
	model.addConstr( outxor1 == outS51[[1,4,0]] + outS3c1, name				    = "(%d,%d)/xor1"%(rounds,col))

	# S5_2
	inS52 = model.addMVar(shape = 5, vtype = GRB.BINARY, name					= "(%d,%d)/inS52"%(rounds,col))
	#copy 3-bit of input of S52
	model.addConstr(inS52[:3] + outVar[[0,6,5]] == outxor1[[1,2,0]], name	    = "(%d,%d)/copyinS52"%(rounds,col))
	#locate 2-bit of input of S52
	model.addConstr(inS52[3:] == outS51[[2,3]], name							= "(%d,%d)/locinS52"%(rounds,col))
	outS52 = model.addMVar(shape = 5, vtype = GRB.BINARY, name 					= "(%d,%d)/outS52"%(rounds,col))
	sboxConstr(model, inS52, outS52, ineqs['S52K'], constrname					= "(%d,%d)/S52"%(rounds,col))
	#inS52 --S52-> outS52

	# XOR2 and locate (bit permutation)
	model.addConstr( outS52[:3] + outS3c2[[2,0,1]] == outVar[[2,1,7]], name		= "(%d,%d)/TrXOR"%(rounds,col))
	model.addConstr( outS52[3:] == outVar[[4,3]])


def milpPIPO(rounds, indiv, outdiv, modelname = None):
	# start gurobi
	try:
		# Create Model
		model = gp.Model()

		# ================ ( 1 ) round ================			# ================ ( R ) round ================	
		# X[0] --- Sbox ---> Y[0] --- Perm ---> X[1]			# X[R-1] --- Sbox ---> Y[R-1] --- Perm ---> X[R]	
		X = [model.addMVar(shape = blocksize, vtype=GRB.BINARY, name="x%d"%r) for r in range(rounds + 1)]
		Y = [model.addMVar(shape = blocksize, vtype=GRB.BINARY, name="y%d"%r) for r in range(rounds)]

		# Set initial, output div
		indiv = np.array([(indiv>>i)&1 for i in range(blocksize)])
		outdiv = np.array([(outdiv>>i)&1 for i in range(blocksize)])
		model.addConstr(X[0] == indiv, name = "Init")
		model.addConstr(X[rounds] == outdiv, name = "Out")
		
		# Object function : Min(X[rounds][0] + ... ~ ... + X[rounds][63]) 
		obj = np.array([1.0 for x in range(blocksize)])
		model.setObjective(obj @ X[rounds], GRB.MINIMIZE)

		columns = np.array([x for x in range(64)]).reshape(8,8)

		for r in range(rounds):
			# sbox
			for col in range(blocksize//sboxsize):
				piposboxConstr(model, X[r][ columns[:,col] ], Y[r][ columns[:,col] ], r, col)

			# bit perm
			model.addConstr(Y[r] == X[r+1][BP], name = "%d/Perm"%r)

		model.optimize()
		if modelname:
			model.write(modelname)
		if model.Status == GRB.OPTIMAL:	# If exist sol
			return 'u'
		elif model.Status == GRB.INFEASIBLE:
			return 'b'
		else:
			print("Unknown Error")

	except gp.GurobiError as e:
	    print('Error code ' + str(e.errno) + ": " + str(e))

	except AttributeError:
	    print('Encountered an attribute error')