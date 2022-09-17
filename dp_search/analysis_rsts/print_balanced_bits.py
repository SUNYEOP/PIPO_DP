import os, sys
import pickle
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "prep_util"))
from sbox import *
from sboxes import *
target = SBOX_DICTIONARY['PIPO']


def hex_to_vec(hex):
    out = []
    for bidx in range(8):
        if hex.__and__(1) == 1:
            out.append(1)
        else:
            out.append(0)
        hex = hex >> 1
    out.reverse()
    return tuple(out)

def in_str(vin):
    out_str = ""
    re_vin = reversed(vin)
    for bidx, coef in enumerate(re_vin):
        if coef == 1:
            out_str += "x_{%d,i} ^ "%(bidx)
    return out_str[:-3]

R_layer = [0, 7, 4, 3, 6, 5, 1, 2]

def ou_str(j, vout):
    out_str = ""
    re_vout = reversed(vout)
    for bidx, coef in enumerate(re_vout):
        if coef == 1:
            out_str += "x_{%d,%d+i} ^ "%(bidx, (j + R_layer[bidx]) % 8)
    return out_str[:-3]

print("##############################################################################")
print("###                        QM 6R balanced Bits                          ######")
print("##############################################################################")

with open("result_qm", 'rb') as f:
    results = pickle.load(f)
bals = []
for invec in results.keys():
    for col in range(8):
        for u in range(1, 1<<target.outbit):
            comp = target.component(u)
            monos = comp.get_monomials()
            for mono in monos:
                if results[invec][col][mono] == False:
                    break
            else:
                bals.append((invec, col, u))

print("In".center(30), " ==6R> ", "Out".center(30))
print("------------------------------------------------------------------------------")

for tup in bals:
    vin  = hex_to_vec(tup[0])
    j    = tup[1]
    vout = hex_to_vec(tup[2])
    print(in_str(vin).center(30), " ==6R> ", ou_str(j, vout).center(30))

print("##############################################################################")
print("!!! Note !!!")
print("x_{0,2+i} ^ x_{1,1+i} ^ x_{5,7+i} ^ x_{6,3+i} can be construced from x_{0,2+i} ^ x_{1,1+i} ^ x_{6,3+i} and x_{5,7+i}")
print("x_{0,3+i} ^ x_{1,2+i} ^ x_{5,0+i} ^ x_{6,4+i} can be construced from x_{0,3+i} ^ x_{1,2+i} ^ x_{6,4+i} and x_{5,0+i}")
print("##############################################################################")

print()
print("##############################################################################")
print("###                    Struct 6R balanced Bits                          ######")
print("##############################################################################")

with open("result_struct", 'rb') as f:
    results = pickle.load(f)
bals = []
for invec in results.keys():
    for col in range(8):
        for u in range(1, 1<<target.outbit):
            comp = target.component(u)
            monos = comp.get_monomials()
            for mono in monos:
                if results[invec][col][mono] == False:
                    break
            else:
                bals.append((invec, col, u))

print("In".center(30), " ==6R> ", "Out".center(30))
print("------------------------------------------------------------------------------")

for tup in bals:
    vin  = hex_to_vec(tup[0])
    j    = tup[1]
    vout = hex_to_vec(tup[2])
    print(in_str(vin).center(30), " ==6R> ", ou_str(j, vout).center(30))
