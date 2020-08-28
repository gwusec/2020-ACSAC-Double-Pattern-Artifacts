#!/usr/bin/env python

import os,sys,random,getopt
import markov
import numpy as np

USAGE = """./guess.py [OPTIONS] data.txt

Perform a cross-fold validation guessing estimation using a markov estimator. 

-f folds    \t how many cross-folds (dflt: 4)
-r repeats  \t how many repititions of a cross fold (dflt: 2)
-m maxguess \t maximum number of guesses to make 
-n grams    \t n-gram size (dflt: 3)
-g file.txt \t use this guessing list instead of generating 
-s states   \t how many states to use (dflt: 9)
-b blacklist\t list of blacklisted codes not to guess
-?          \t sort only on model
-x training \t use this file as extra training
"""

def gen_folds(data,nfolds):
    random.shuffle(data)

    size = len(data)/nfolds
    folds = []
    for i in range(nfolds):
        folds.append(data[i*size:(i+1)*size])
        
    #any extra put in last fold
    folds[-1].extend(data[nfolds*size:]) 
    
    return folds

def load_data(data_f):
    codes = []
    for l in open(data_f):
        if "." in l:
            codes.append(map(int,l.strip().split(".")))
        else:
            codes.append(map(int,l.strip()))
    return codes

def frequencies(data,extra_codes=None):
    freq = {}
    for d in data:
        d = tuple(d)
        freq.setdefault(d,0)
        freq[d]+=1

    if extra_codes:
        for d in extra_codes:
            freq.setdefault(tuple(d),0)

    return freq

if __name__ == "__main__":
    nfolds = 4
    repeats = 2
    maxguesses = None
    guess_codes = None
    states = 9
    grams = 3
    blacklist = None
    model_only = None
    xtraining = None

    opts,args = getopt.getopt(sys.argv[1:], "f:r:m:g:n:hs:b:?x:")
    for o,a in opts:
        if o == "-h":
            print USAGE
            exit(0)
        elif o == "-f":
            nfolds = int(a)
        elif o == "-r":
            repeats = int(a)
        elif o == "-m":
            maxguesses = int(a)
        elif o == "-g":
            print >>sys.stderr, "...Loading Guessing File"
            guess_codes = load_data(a)
        elif o == "-n":
            grams = int(a)
        elif o == "-s":
            states = int(a)
        elif o == "-b":
            blacklist = load_data(a)
        elif o == "-?":
            model_only = True
        elif o == "-x":
            xtraining = load_data(a)

        else:
            print "ERROR: unknown option '%s'"%(o)
            exit(1)

    
    codes = load_data(args[0])

    
    folds = gen_folds(codes,nfolds)
    results = []
    for r in range(repeats):
        
        for f in range(nfolds):
            print >>sys.stderr, "Repeat: %d Fold %d/%d"%(r+1,f+1,nfolds)



            test = folds[f]
            train = []
            for j in range(nfolds):
                if j != f:
                    folds[j]
                    train.extend(folds[j])
            

            #include extra training data
            if xtraining:
                train.extend(xtraining)

            print >>sys.stderr, "... Building Model"
            len_table = markov.build_len_table(train)
            trans_table = markov.build_trans_table(train,states,grams)
            start_table = markov.build_start_table(train,states)
            end_table = markov.build_end_table(train,states)

            
            print >>sys.stderr, "... Computing Strength"

            #use file or training data
            input_codes = train if not guess_codes else guess_codes
            
            
            strength = dict((tuple(c),p) for c,p in markov.strength(input_codes,grams,len_table,start_table,end_table,trans_table,20))

            print >>sys.stderr, "... Computing Frequencies"
            freq = frequencies(train,guess_codes)


            to_guess = dict((tuple(c),None) for c in input_codes) #start as dict to avoid duplication
            
            if blacklist:
                print >>sys.stderr, "... Removing blacklisted"
                for d in blacklist:
                    to_guess.pop(tuple(d))

            print >>sys.stderr, "... Sorting"

            guess_list = to_guess.keys()
            #sort all training based on inverse frequencie and markov strength
            if not model_only:
                guess_list.sort(cmp=lambda a,b: -cmp(freq[a],freq[b]) if freq[a] != freq[b] else cmp(strength[a],strength[b]))
            else:
                guess_list.sort(cmp=lambda a,b: cmp(strength[a],strength[b]))

            test_freq = frequencies(test)

            res = []
            i = 0
            guessed = 0
            total = float(len(test))
            for g in guess_list:
                i+=1
                if g in test_freq:
                    guessed += test_freq[g]

                res.append(guessed/total)

                if maxguesses and i > maxguesses:
                    break

            results.append(res)

    for i in range(min(map(len,results))):
        print i+1, np.mean([r[i] for r in results])
