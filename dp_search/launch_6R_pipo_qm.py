import os, sys, pickle
import numpy as np
from timeit import default_timer as timer
from datetime import timedelta

# Preperation
with open("front_gen/lambPIPO", 'rb') as f:
    lambs = pickle.load(f)
with open("front_gen/front_tablePIPO", 'rb') as f:
    front_table = pickle.load(f)


setbit0 = lambda k,i: k &( ~ (1<<i))
setbit1 = lambda k,i: k | (1<<i)
target_col = 0
colidxs = [8*i + target_col for i in range(8)]
hw_order = sorted([x for x in range(1, 1<<8)], key = lambda x: bin(x).count('1'))
sboxsize = 8
mask = (1<<64)-1
r = 6


def makeFalse(li, k, bitsize):
    zerobits = [1<<x for x in range(bitsize) if (k>>x)&1 == 0]
    succs = [k + sum([zerobits[x] for x in range(len(zerobits)) if (idx>>x)&1]) for idx in range(1,1<<len(zerobits))]
    for x in succs:
        li[x] = False


### PIPO QM - 6R#
 
import pipo_qm
start = timer()

milpPIPO = pipo_qm.milpPIPO
# Working code
results = []
for propagated_values in front_table[lambs]:
    # 1-R using front table
    K = set()
    for k in propagated_values: # k : 1-st round 0-th S-box o linear
        temp = mask
        for i in range(8):
            if (k>>i)&1 == 0:
                temp = setbit0(temp, pipo_qm.BP[8*i])
        K.add(temp)
    result_col = dict()
    # 2 ~ R-1
    for col in range(8):
        output_monos = np.array([True for x in range(1<<sboxsize)]); output_monos[0] = False
      
        for indiv in K:
            for outdiv in hw_order:
                if output_monos[outdiv] == False:
                    continue
              
                outdiv64 = 0
                for i in range(8):
                    if (outdiv>>i) & 1:
                        outdiv64 = setbit1(outdiv64, 8*i + col)
                flag = milpPIPO(r-2, indiv, outdiv64)
                if flag == 'u':
                    output_monos[outdiv] = False
                    makeFalse(output_monos, outdiv, 8) # for x> outdiv, temp[x] = False
        result_col[col] = output_monos
    results.append(result_col)
results = dict(zip(lambs, results))
with open("result_qm", 'wb') as f:
    pickle.dump(results, f)
end = timer()
total_time = timedelta(seconds=end-start)
with open("result_qmtime.txt", 'w') as f:
    f.write("WorkingTime: {} sec".format(timedelta(seconds=end-start)))
print("WorkingTime: {} sec".format(timedelta(seconds=end-start)))