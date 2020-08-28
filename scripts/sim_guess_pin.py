#!/usr/bin/env python3

"""

This will do a simulated guess n times, downsampled to x. Optionally, you can include a blacklist

"""

import os,sys,random,getopt

from sim_guess_2patt import do_guess,load_to_guess,load_guess_l

import numpy as np

USAGE = """./sim-guess-pin-normed.py patterns-to-guess pattern-frequency

Perform a cross-fold validation guessing estimation using a markov estimator. 

-n repetitions\t how many repititions (dflt:50)
-x downsample \t what downsample size (dflt: None)
-m max        \t max number of guesses (dflt: unlimitted)
-o output     \t where to send output
Sample command

./sim_guess_pin_normed -n 50 -x 200  patts/pin/allfirstentry.4digit.txt   patts/pin/amitay.4digit-withcount.txt
"""

if __name__ == "__main__":


    reps = 50
    downsample = None
    output = sys.stdout
    max_guesses = None


    opts,args = getopt.getopt(sys.argv[1:], "n:x:ho:m:")
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
        elif o == "-o":
            output = open(a,"w")
        else:
            print("ERROR: unknown option '{}'".format(o))
            exit(1)


    dpatt_f = args[0]
    freq_f = args[1]

    print("... Loading Patterns To-Guess", file=sys.stderr)
    to_guess = [l.strip() for l in open(dpatt_f)]


    print("... Loading Guessing List", file=sys.stderr)
    guess_l = []
    for l in open(freq_f):
        f,p = l.strip().split(" ")
        guess_l.append((p,f))

        if max_guesses and len(guess_l) >= max_guesses:
            print("\t... trimming down to {} guesses".format(max_guesses),file=sys.stderr)
        #    guess_l = guess_l[:max_guesses if max_guesses < len(guess_l) else len(guess_l)-1]
            break
        

    print(max_guesses, len(guess_l))
    if not downsample or downsample > len(to_guess):
        downsample = len(to_guess)

    print("... Guessing")
    
#    print(guess_l[:10])
    all_res = {}
    for r in range(reps):
        print("... rep {}/{}".format(r+1,reps), file=sys.stderr)

        r_to_guess = random.sample(to_guess, downsample)
#        print(r_to_guess[:10])
        n = float(len(r_to_guess))
        to_guess_freq = {}
        for p1 in r_to_guess:
            to_guess_freq.setdefault(p1,0)
            to_guess_freq[p1]+=1

#        print(to_guess_freq)

        res = [(0,0.0)]
        for p1,freq in guess_l:
            g = res[-1][0] + 1
            last_p = res[-1][1]

            if p1 in to_guess_freq:
                new_p = last_p + to_guess_freq[p1]/n
            else:
                new_p = last_p

            res.append((g,new_p))
            
        for i,perc in res:            
            all_res.setdefault(i,[]).append(perc)


    print("... Calculating Result and Printing Output", file=sys.stderr)

    for i in range(len(all_res)):
        print("{} {} {} {} {}".format(i,
                                   np.mean(all_res[i]),
                                   np.median(all_res[i]),
                                   np.quantile(all_res[i],0.25),
                                   np.quantile(all_res[i],0.75)),
              file=output)
        


