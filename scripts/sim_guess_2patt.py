#!/usr/bin/env python3

"""

This will do a simulated guess n times, downsampled to x. Optionally, you can include a blacklist

"""

import os,sys,random,getopt
import numpy as np

USAGE = """./sim-guess-2patt-normed.py patterns-to-guess pattern-frequency

Perform a cross-fold validation guessing estimation using a markov estimator. 

-n repetitions\t how many repititions (dflt:50)
-x downsample \t what downsample size (dflt: None)
-m max        \t max number of guesses (dflt: unlimitted)
-o output     \t where to send output
--b1 blacklist\t list of first pattern blacklists (dflt:none)
--b2 blacklist\t list of two pattern blacklists (dflt:none)

Sample command

./sim_guess_2patt_normed -n 50 -x 200 --b1 patts/bl/bl_first.txt patts/dpatt/first.txt patts/dpatt/sim-all-rel-freq.txt
"""



def do_guess(to_guess,guess_l):

    n = float(len(to_guess))
    
    to_guess_freq = {}
    for p1,p2 in to_guess:
        to_guess_freq.setdefault((p1,p2),0)
        to_guess_freq[(p1,p2)]+=1

    res = [(0,0.0)]
    for p1,p2,freq in guess_l:
        g = res[-1][0] + 1
        last_p = res[-1][1]

        if (p1,p2) in to_guess_freq:
            new_p = last_p + to_guess_freq[(p1,p2)]/n
        else:
            new_p = last_p

        res.append((g,new_p))
    return res

def load_guess_l(freq_f):
    guess_l = []
    for  l in open(freq_f):
        (p1,p2,freq) = l.strip().split(" ")
        guess_l.append((tuple(p1.split(".")),tuple(p2.split(".")), int(freq)))
    return guess_l

def load_to_guess(dpatts_f):
    to_guess = []
    for l in open(dpatts_f):
        p1,p2 = l.strip().split(" ")
        p1,p2 = tuple(p1),tuple(p2)
        to_guess.append((p1,p2))
    return to_guess



if __name__ == "__main__":


    reps = 50
    downsample = None
    bfirst_f = None
    bsecond_f = None
    output = sys.stdout
    max_guesses = None

    opts,args = getopt.getopt(sys.argv[1:], "n:x:ho:m:",["b1=","b2="])
    for o,a in opts:
        if o == "-h":
            print(USAGE)
            exit(0)
        elif o == "-n":
            reps = int(a)
        elif o == "-x":
            downsample = int(a)
        elif o == "-m":
            max_guesses = int(a)
        elif o == "--b1":
            bfirst_f = a
        elif o == "--b2":
            bsecond_f = a
        elif o == "-o":
            output = open(a,"w")
        else:
            print("ERROR: unknown option '{}'".format(o))
            exit(1)

    if bfirst_f and bsecond_f:
        print("ERROR: only --b1 or --b2 options can be used, not both")
        exit(1)


    if len(args) < 2:
        print("ERROR: require to_guess and frequency list")
        exit(1)

    dpatt_f = args[0]
    freq_f = args[1]

    print("... Loading Patterns To-Guess", file=sys.stderr)
    to_guess = load_to_guess(dpatt_f)

    print("... Loading Guessing List", file=sys.stderr)
    if not bfirst_f and not bsecond_f:
        guess_l = load_guess_l(freq_f)
    else:
        print("\t... and removeing blacklist", file=sys.stderr)
        if bfirst_f:
            blacklist = {}
            for l in open(bfirst_f):
                p = tuple(l.strip().split("."))
                blacklist[p]=True

        if bsecond_f:
            blacklist = {}
            for l in open(bsecond_f):
                p1,p2 = l.strip().split(" ")
                p1 = tuple(l.split("."))
                p2 = tuple(l.split("."))
                blacklist[(p1,p2)]=True

        guess_l=[]
        for l in open(freq_f):
            p1,p2,f = l.strip().split(" ")
            p1 = tuple(p1.split("."))
            p2 = tuple(p2.split("."))
            if bfirst_f and not blacklist.get(p1,False):
                guess_l.append((p1,p2,f))
            if bsecond_f and not blacklist.get((p1,p2),False):
                guess_l.append((p1,p2,f))

        if max_guesses:
            print("\t... trimming down to {} guesses".format(max_guesses),file=sys.stderr)
            guess_l = guess_l[:max_guesses if max_guesses < len(guess_l) else len(guess_l)-1]

    if not downsample or downsample > len(to_guess):
        downsample = len(to_guess)

    print("... Guessing")
    
    all_res = {}
    for r in range(reps):
        print("... rep {}/{}".format(r+1,reps))

        r_to_guess = random.sample(to_guess, downsample)
        res = do_guess(r_to_guess,guess_l)

        for i,perc in res:            
            all_res.setdefault(i,[]).append(perc)


    print("... Calculating Result and Printing Output")

    for i in range(len(all_res)):
        print("{} {} {} {} {}".format(i,
                                   np.mean(all_res[i]),
                                   np.median(all_res[i]),
                                   np.quantile(all_res[i],0.25),
                                   np.quantile(all_res[i],0.75)),
              file=output)
        


