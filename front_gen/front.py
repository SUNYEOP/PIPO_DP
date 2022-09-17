# Add directory of mymodule to sys.path
import numpy as np; import os, sys, pickle
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "prep_util"))
from sbox import *
from sboxes import *

def reduce(K):  # remove redundant k' in K
    for bigk in list(K):
        for k in K:
            if (k != bigk ) & (k&bigk == k): # if exist k s.t. bigk > k
                K.remove(bigk)
                break

def get_fronttable(sbox):
    n = sbox.outbit
    maxmonos = [(1<<n)-1-(1<<k) for k in range(n)]

    alphas = []
    for u in range(1<<n):
        p = sbox.product(u)
        if u==(1<<n)-1:
            alpha = [0 for mono in maxmonos]
        else:
            alpha = [(p.ANF>>mono)&1 for mono in maxmonos] # Check there are mono in p
        alphas.append(alpha)
    alphas = np.array(alphas)

    front_table = [[]]
    for lamb in range(1,1<<n):
        veclamb = np.array([(lamb>>i)&1 for i in range(n)])
        row = [v for v in range(len(alphas)) if (veclamb@alphas[v])%2]
        reduce(row)
        front_table.append(row)
    return np.array(front_table)

def is_superset(subset, superset): # Return whether Succ(superset) is superset of Succ(subset)
# The condition is that : for all k in subset, exist smallk in superset s.t. k>=smallk
    issmaller = lambda small, big: (small & big) == small
    for k in subset:
        if not True in [issmaller(smallk, k) for smallk in superset]: # if not exist smallk
            return False
    return True

def pruningKin(front_table):
    subsetflag = [True for x in range(len(front_table))]
    subsetflag[0] = False

    for sup in range(1,len(front_table)):
        for sub in np.where(subsetflag)[0]:
            if sup == sub:
                continue
            if is_superset(front_table[sub],front_table[sup]):
                subsetflag[sup] = False
    return np.where(subsetflag)[0]


if __name__ == "__main__":
    s = SBOX_DICTIONARY['PIPO']
    front_table = get_fronttable(s)
    lamb = pruningKin(front_table)
    f = open("front_table" + "PIPO", 'wb')
    pickle.dump(front_table, f)
    f.close()
    
    g = open("lamb" + "PIPO", 'wb')
    pickle.dump(lamb, g)
    g.close()