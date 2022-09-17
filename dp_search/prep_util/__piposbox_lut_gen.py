# Result======================================================
S3	=	[0x4,	0x7,	0x5,	0x0,	0x3,	0x2,	0x1,	0x6]
S51	=	[
0x0,	0x9,	0x17,	0x1c,	0x5,	0x1a,	0x13,	0xe,	0x8,	0x1,	0x1d,	0x16,	0xf,	0x12,	0x1b,	0x4,	
0x14,	0x1f,	0x3,	0xa,	0x11,	0xc,	0x7,	0x18,	0x19,	0x6,	0xd,	0x10,	0x1e,	0x15,	0xb,	0x2]
S52	=	[
0x0,	0x1,	0x1a,	0x1f,	0x1c,	0x1d,	0x1e,	0x1b,	0xa,	0x12,	0x10,	0x8,	0x16,	0x6,	0x14,	0x4,	
0x19,	0x18,	0x7,	0x2,	0xd,	0xc,	0xb,	0xe,	0x17,	0xf,	0x9,	0x11,	0x3,	0x13,	0x5,	0x15]
S8	=	[
0x5e,	0xf9,	0xfc,	0x0,	0x3f,	0x85,	0xba,	0x5b,	0x18,	0x37,	0xb2,	0xc6,	0x71,	0xc3,	0x74,	0x9d,	
0xa7,	0x94,	0xd,	0xe1,	0xca,	0x68,	0x53,	0x2e,	0x49,	0x62,	0xeb,	0x97,	0xa4,	0xe,	0x2d,	0xd0,	
0x16,	0x25,	0xac,	0x48,	0x63,	0xd1,	0xea,	0x8f,	0xf7,	0x40,	0x45,	0xb1,	0x9e,	0x34,	0x1b,	0xf2,	
0xb9,	0x86,	0x3,	0x7f,	0xd8,	0x7a,	0xdd,	0x3c,	0xe0,	0xcb,	0x52,	0x26,	0x15,	0xaf,	0x8c,	0x69,	
0xc2,	0x75,	0x70,	0x1c,	0x33,	0x99,	0xb6,	0xc7,	0x4,	0x3b,	0xbe,	0x5a,	0xfd,	0x5f,	0xf8,	0x81,	
0x93,	0xa0,	0x29,	0x4d,	0x66,	0xd4,	0xef,	0xa,	0xe5,	0xce,	0x57,	0xa3,	0x90,	0x2a,	0x9,	0x6c,	
0x22,	0x11,	0x88,	0xe4,	0xcf,	0x6d,	0x56,	0xab,	0x7b,	0xdc,	0xd9,	0xbd,	0x82,	0x38,	0x7,	0x7e,	
0xb5,	0x9a,	0x1f,	0xf3,	0x44,	0xf6,	0x41,	0x30,	0x4c,	0x67,	0xee,	0x12,	0x21,	0x8b,	0xa8,	0xd5,	
0x55,	0x6e,	0xe7,	0xb,	0x28,	0x92,	0xa1,	0xcc,	0x2b,	0x8,	0x91,	0xed,	0xd6,	0x64,	0x4f,	0xa2,	
0xbc,	0x83,	0x6,	0xfa,	0x5d,	0xff,	0x58,	0x39,	0x72,	0xc5,	0xc0,	0xb4,	0x9b,	0x31,	0x1e,	0x77,	
0x1,	0x3e,	0xbb,	0xdf,	0x78,	0xda,	0x7d,	0x84,	0x50,	0x6b,	0xe2,	0x8e,	0xad,	0x17,	0x24,	0xc9,	
0xae,	0x8d,	0x14,	0xe8,	0xd3,	0x61,	0x4a,	0x27,	0x47,	0xf0,	0xf5,	0x19,	0x36,	0x9c,	0xb3,	0x42,	
0x1d,	0x32,	0xb7,	0x43,	0xf4,	0x46,	0xf1,	0x98,	0xec,	0xd7,	0x4e,	0xaa,	0x89,	0x23,	0x10,	0x65,	
0x8a,	0xa9,	0x20,	0x54,	0x6f,	0xcd,	0xe6,	0x13,	0xdb,	0x7c,	0x79,	0x5,	0x3a,	0x80,	0xbf,	0xde,	
0xe9,	0xd2,	0x4b,	0x2f,	0xc,	0xa6,	0x95,	0x60,	0xf,	0x2c,	0xa5,	0x51,	0x6a,	0xc8,	0xe3,	0x96,	
0xb0,	0x9f,	0x1a,	0x76,	0xc1,	0x73,	0xc4,	0x35,	0xfe,	0x59,	0x5c,	0xb8,	0x87,	0x3d,	0x2,	0xfb]
# ======================================================

import os
import sys
nowdir = os.getcwd()
backdir = os.path.dirname(nowdir)
sys.path.append(os.path.abspath(backdir + "\\mymodule"))
from sbox import *

S3 = Sbox(S3); S51 = Sbox(S51); S52 = Sbox(S52); S8 = Sbox(S8)

# ======================================================
def LUTprint(li, rowlength = 16):
	n = len(li)
	if n <= rowlength:
		print("[", end = '')
		for x in range(n):
			print(li[x], end = '')
			if x != (n-1):
				print(end = ",\t")
		print("]")
		return 

	print("[", end = '\n')
	for x in range(n):
		print(li[x], end = '')
		if x != (n-1):
			print(end = ",\t")
		else:
			print("]")
		if (x!=1)&(x!=(n-1))&(x%rowlength == 15):
			print()
# ======================================================

# ======================================================
# S3 make
def S3make():
	s, n = [], 3
	for x in range(1<<n):
		X = [1&(x>>i) for i in range(n)]
		X[2] ^= X[1] & X[0];
		X[0] ^= X[2] | X[1];
		X[1] ^= X[2] | X[0];
		X[2] = int(not X[2]);
		s.append(hex(sum([1<<i for i in range(n) if X[i]])))
	LUTprint(s)
# ======================================================

# ======================================================
# S51 make
def S51make():
	s, n = [], 5
	for x in range(1<<n):
		X = [0,0,0] + [1&(x>>i) for i in range(n)]

		X[5] ^= (X[7] & X[6]);
		X[4] ^= (X[3] & X[5]);
		X[7] ^= X[4];
		X[6] ^= X[3];
		X[3] ^= (X[4] | X[5]);
		X[5] ^= X[7];
		X[4] ^= (X[5] & X[6]);

		X = X[3:]
		s.append(hex(sum([1<<i for i in range(n) if X[i]])))
	LUTprint(s)
# ======================================================

# ======================================================
# S52 make
def S52make():
	s, n = [], 5
	for x in range(1<<n):
		X = [1&(x>>i) for i in range(n)]
		T = X[:3]; X[5:7] = X[3:5]
		# X = [0,0,0] + [1&(x>>i) for i in range(n)]
		# T = [0,0,0]
		# T[0] = X[7];	T[1] = X[3];	T[2] = X[4];
		X[6] ^= (T[0] & X[5]);
		T[0] ^= X[6];
		X[6] ^= (T[2] | T[1]);
		T[1] ^= X[5];
		X[5] ^= (X[6] | T[2]);
		T[2] ^= (T[1] & T[0]);

		X = T + X[5:7]
		s.append(hex(sum([1<<i for i in range(n) if X[i]])))
	LUTprint(s)
# ======================================================

# ======================================================
# S8 make
def S8make():
	s, n = [], 8
	for x in range(1<<n):
		X = [1&(x>>i) for i in range(n)]
		T = [0,0,0]

		# //S5_1
		X[5] ^= (X[7] & X[6]);
		X[4] ^= (X[3] & X[5]);
		X[7] ^= X[4];
		X[6] ^= X[3];
		X[3] ^= (X[4] | X[5]);
		X[5] ^= X[7];
		X[4] ^= (X[5] & X[6]);
		# //S3
		X[2] ^= X[1] & X[0];
		X[0] ^= X[2] | X[1];
		X[1] ^= X[2] | X[0];
		X[2] = int(not X[2]);
		# // Extend XOR
		X[7] ^= X[1];	X[3] ^= X[2];	X[4] ^= X[0];
		# //S5_2
		T[0] = X[7];	T[1] = X[3];	T[2] = X[4];
		X[6] ^= (T[0] & X[5]);
		T[0] ^= X[6];
		X[6] ^= (T[2] | T[1]);
		T[1] ^= X[5];
		X[5] ^= (X[6] | T[2]);
		T[2] ^= (T[1] & T[0]);
		# // Truncate XOR and bit change
		X[2] ^= T[0];	T[0] = X[1] ^ T[2];	X[1] = X[0]^T[1];	X[0] = X[7];	X[7] = T[0];
		T[1] = X[3];	X[3] = X[6];	X[6] = T[1];
		T[2] = X[4];	X[4] = X[5];	X[5] = T[2];

		s.append(hex(sum([1<<i for i in range(n) if X[i]])))
	LUTprint(s)
# ======================================================

# ======================================================
# S3LUT validation
def validS3():
	s, n = [], 8
	for x in range(1<<n):
		X = [1&(x>>i) for i in range(n)]
		T = [0,0,0]

		# //S5_1
		X[5] ^= (X[7] & X[6]);
		X[4] ^= (X[3] & X[5]);
		X[7] ^= X[4];
		X[6] ^= X[3];
		X[3] ^= (X[4] | X[5]);
		X[5] ^= X[7];
		X[4] ^= (X[5] & X[6]);
		# //S3
		newx = sum([1<<i for i in range(3) if X[i]])			# X[2] ^= X[1] & X[0];
		newx = S3.LUT[newx]										# X[0] ^= X[2] | X[1];
		for i in range(3):										# X[1] ^= X[2] | X[0];
			X[i] = 1&(newx>>i)									# X[2] = int(not X[2]);

		# // Extend XOR
		X[7] ^= X[1];	X[3] ^= X[2];	X[4] ^= X[0];
		# //S5_2
		T[0] = X[7];	T[1] = X[3];	T[2] = X[4];
		X[6] ^= (T[0] & X[5]);
		T[0] ^= X[6];
		X[6] ^= (T[2] | T[1]);
		T[1] ^= X[5];
		X[5] ^= (X[6] | T[2]);
		T[2] ^= (T[1] & T[0]);
		# // Truncate XOR and bit change
		X[2] ^= T[0];	T[0] = X[1] ^ T[2];	X[1] = X[0]^T[1];	X[0] = X[7];	X[7] = T[0];
		T[1] = X[3];	X[3] = X[6];	X[6] = T[1];
		T[2] = X[4];	X[4] = X[5];	X[5] = T[2];

		out = sum([1<<i for i in range(n) if X[i]])
		if S8.LUT[x] != out:
			print(x)
			break
	else:
		print("S3 Good")
# validS3()
# ======================================================

# ======================================================
# S51LUT validation
def validS51():
	s, n = [], 8
	for x in range(1<<n):
		X = [1&(x>>i) for i in range(n)]
		T = [0,0,0]

		# //S5_1
		newx = sum([1<<i for i in range(5) if X[3:][i]])	# X[5] ^= (X[7] & X[6]);
		newx = S51.LUT[newx]								# X[4] ^= (X[3] & X[5]);
		for i in range(5):									# X[7] ^= X[4];
			X[3+i] = 1&(newx>>i)							# X[6] ^= X[3];
															# X[3] ^= (X[4] | X[5]);
															# X[5] ^= X[7];
															# X[4] ^= (X[5] & X[6]);
		# //S3
		X[2] ^= X[1] & X[0];
		X[0] ^= X[2] | X[1];
		X[1] ^= X[2] | X[0];
		X[2] = int(not X[2]);
		# // Extend XOR
		X[7] ^= X[1];	X[3] ^= X[2];	X[4] ^= X[0];
		# //S5_2
		T[0] = X[7];	T[1] = X[3];	T[2] = X[4];
		X[6] ^= (T[0] & X[5]);
		T[0] ^= X[6];
		X[6] ^= (T[2] | T[1]);
		T[1] ^= X[5];
		X[5] ^= (X[6] | T[2]);
		T[2] ^= (T[1] & T[0]);
		# // Truncate XOR and bit change
		X[2] ^= T[0];	T[0] = X[1] ^ T[2];	X[1] = X[0]^T[1];	X[0] = X[7];	X[7] = T[0];
		T[1] = X[3];	X[3] = X[6];	X[6] = T[1];
		T[2] = X[4];	X[4] = X[5];	X[5] = T[2];

		out = sum([1<<i for i in range(n) if X[i]])
		if S8.LUT[x] != out:
			print(x)
			break
	else:
		print("S51 Good")
# validS51()
# ======================================================

# ======================================================
# S52LUT validation
def validS52():
	s, n = [], 8
	for x in range(1<<n):
		X = [1&(x>>i) for i in range(n)]
		T = [0,0,0]

		# //S5_1
		X[5] ^= (X[7] & X[6]);
		X[4] ^= (X[3] & X[5]);
		X[7] ^= X[4];
		X[6] ^= X[3];
		X[3] ^= (X[4] | X[5]);
		X[5] ^= X[7];
		X[4] ^= (X[5] & X[6]);
		# //S3
		X[2] ^= X[1] & X[0];
		X[0] ^= X[2] | X[1];
		X[1] ^= X[2] | X[0];
		X[2] = int(not X[2]);
		# // Extend XOR
		X[7] ^= X[1];	X[3] ^= X[2];	X[4] ^= X[0];
		# //S5_2
		T[0] = X[7];	T[1] = X[3];	T[2] = X[4];
		li = T + X[5:7]
		newx = sum([1<<i for i in range(5) if li[i]])	# X[6] ^= (T[0] & X[5]);
		newx = S52.LUT[newx]							# T[0] ^= X[6];
		for i in range(3):								# X[6] ^= (T[2] | T[1]);
			T[i] = 1&(newx>>i)							# T[1] ^= X[5];
		for i in range(3,5):							# X[5] ^= (X[6] | T[2]);
			X[2 + i] = 1&(newx>>i)						# T[2] ^= (T[1] & T[0]);
		# // Truncate XOR and bit change
		X[2] ^= T[0];	T[0] = X[1] ^ T[2];	X[1] = X[0]^T[1];	X[0] = X[7];	X[7] = T[0];
		T[1] = X[3];	X[3] = X[6];	X[6] = T[1];
		T[2] = X[4];	X[4] = X[5];	X[5] = T[2];

		out = sum([1<<i for i in range(n) if X[i]])
		if S8.LUT[x] != out:
			print(x)
			break
	else:
		print("S52 Good")
# validS52()
# ======================================================

t = S8.get_DPT()[0]
cnt = 0
for a in t:
	cnt += len(a)
print(cnt)