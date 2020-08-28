#!/usr/bin/env python3
import math, operator, sys
import os.path
import numpy as np
import json as js

probs = []
p_size = 30
rounds = 500
min_size = 209
# t_order = ["control","first","both","ideal","all_rel","4x4","4pin","6pin"]
# t_title = ["Control","Blacklist First","Blacklist Both","Ideal Choice","All Related Data","4x4 Grid Expansion","First-4","First-6"]
# treatment = {"ideal":{},
#              "control":{},
#              "first":{},
#              "both":{},
#              "all_rel":{},
#              "4x4":{},
#              "6pin":{},
#              "4pin":{}}

keys = ["β3","β10","β30","H","G5","G10","G20","prob"]
treatment = {}
for st in keys:
    treatment[st] = []

def b_suc(freq,B):
    return 100*sum(freq[:B])/sum(freq)

def a_work(p,a):
    for prob in p:
        if(prob[1] > a):
            return prob[0],prob[1]

def g_alph(prob,a,lam):
    return (1-lam)*a + sum(p*i for [p,i] in prob[:a])

def g_bit(g,lam):
    return math.log((2*g/lam)-1)+math.log(1/(2-lam))

def tukeys(vals):
    q1,q3 = np.percentile(vals, [25,75]) 
    iqr = q3-q1
    low = q1 - (iqr*1.5)
    up = q3 + (iqr*1.5)
    return np.where((vals > up) | (vals < low))


if __name__ == "__main__":

    data_f = sys.argv[1]
    title = sys.argv[2]

    all_patts = [l.strip() for l in open(data_f)]
    t_size = len(all_patts)


    for i in range(rounds):
        patts = np.random.choice(all_patts,size=min_size,replace=False).tolist()    
        all_prob = []
        d = dict()
        for i in patts:
            x=patts.count(i)
            d.update({i:x})
    
        sorted_d = sorted(d.items(), key=operator.itemgetter(1), reverse=True)
        freq = [p[1] for p in sorted_d]
        p = []
        for i in range(1,len(freq)):
            p.append([i,sum(freq[:i])/sum(freq)])

        all_prob.append(p)
        treatment.get("H").append(-math.log(freq[0]/sum(freq)))
        
        for guess in [3,10,30]:
            treatment.get("β"+str(guess)).append(b_suc(freq,guess))
        for perc in [.05,.10,.20]:            
            a,lam = a_work(p,perc)
            g = g_alph(p,a,lam)
            gb = g_bit(g,lam)
            #treatment.get(treat).get("µ"+str(int(perc*100))).append(a)
            treatment.get("G"+str(int(perc*100))).append(gb)
    
    for i in range(0,p_size):
        treatment.get('prob').append(np.mean([x[i][1] for x in all_prob]).tolist())
    s = title + " & " + str(t_size) 
    i  = 0
    for k in keys[:-1]:
        vals = sorted(treatment.get(k))
        inner = np.delete(vals,tukeys(vals))        
        if i < 3:
            s += " & %.2f"%np.mean(inner) + "\% [" + "%.2f"%np.median(inner) + "\%]"
        else:
            s += " & %.2f"%np.mean(inner) + " [" + "%.2f"%np.median(inner) + "]"
        i += 1
    s += " \\"
    s += "\\"    
    print(s)
    

