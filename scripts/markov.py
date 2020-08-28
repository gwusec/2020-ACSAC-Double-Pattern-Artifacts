#!/usr/bin/env python

import os,sys,math,json,getopt
import numpy as np

#Build a simple, smoothed markov model from the input and use it to estimate strength

USAGE="""./markov.py [OPTIONS] data.txt

Print out the strength estimators for the patterns based on the markov model
estimation.

-t train.txt \t use train.txt to train markov mode and teest on data.txt (dflt: data=train)
-s states    \t number of states possible (dflt: 9)
-n grams     \t length of the n-gram (dflt: 3)
-m max       \t max strength value for range of [0,max] (dflt: 20)
"""



def subgrams(c,g): #code and the number of grams
    grams = []
    for i in range(0,len(c)):
        if i + g <= len(c):
            grams.append(tuple(c[i:i+g]))
    return grams


def num_to_gram(n,states,length):
    g = []
    for j in range(0,length):
        g.append(n%states)
        n = n/states
    return tuple(g)

def smooth(states,grams):
    trans_table = {}
    
    #enumerate all grams
    for i in range(0, states**grams):
        g1 = num_to_gram(i,states,grams)
        #add in a possible transition to normal states
        for s in range(0,states):
            g2 = g1[1:] + (s,)
            trans_table.setdefault(g1,{}).setdefault(g2,1)

        #add in a possible transition to an end state
        for s in range(0,states):
            g2 = g1[1:] + (-2,)
            trans_table.setdefault(g1,{}).setdefault(g2,1)

    
    #enumerate all starting state grams
    for g in range(1,grams):
        for i in range(0,states**(grams-g)):
            g1 =  (-1,)*g+num_to_gram(i,states,grams-g)
            for s in range(0,states):
                g2 = g1[1:] + (s,)
                trans_table.setdefault(g1,{}).setdefault(g2,1)

    #enumerate all completing end state grams
    for g in range(1,grams-1):
        for i in range(0,states**(grams-g)):
            g1 =  num_to_gram(i,states,grams-g) + (-2,)*g
            g2 = g1[1:] + (-2,)
            trans_table.setdefault(g1,{}).setdefault(g2,1)
                

    return trans_table


def build_start_table(codes,states=4):
    start_table = dict((s,1) for s in range(states))
    num = len(codes)
    for c in codes:
        start_table.setdefault(c[0],0)
        start_table[c[0]]+=1

    for c in start_table:
        start_table[c]=math.log(start_table[c]/float(num),2)

    return start_table

def build_end_table(codes,states=4):
    end_table = dict((s,1) for s in range(states))
    num = len(codes)
    for c in codes:
        end_table.setdefault(c[-1],0)
        end_table[c[-1]]+=1

    for c in end_table:
        end_table[c]=math.log(end_table[c]/float(num),2)

    return end_table


def build_len_table(codes,maxlen=14):
    num = len(codes)
    len_table = dict((i,1) for i in range(maxlen))

    for c in codes:
        len_table.setdefault(len(c),0)
        len_table[len(c)]+=1


    #normalize length table, store in log so we can do sums later
    for l in len_table:
        len_table[l] = math.log(len_table[l]/float(num),2)
    return len_table

def build_trans_table(codes,states,grams):
    trans_table = smooth(states,grams) #smoothed initialization


    for c in codes:
        #add start and end states
        c = [-1]*(grams-1) + c + [-2]*(grams-1)

        #initialize the transition table
        for g1,g2 in zip(subgrams(c,grams),subgrams(c[1:],grams)):
            g1 = tuple(g1)
            g2 = tuple(g2)
            trans_table[g1][g2]+=1 #won't fail due to smoothing

    #normalize transition table
    for g1 in trans_table:
        tot = sum(trans_table[g1][g2] for g2 in trans_table[g1])
        for g2 in trans_table[g1]:
            trans_table[g1][g2] = math.log(trans_table[g1][g2]/float(tot),2)

    return trans_table


def strength(codes, grams, len_table, start_table, end_table, trans_table, maxstrength):
    res = []
    for c in codes:
        p = len_table[len(c)] + start_table[c[0]] + end_table[c[-1]] #priors
        
        c = [-1]*(grams-1) + c + [-2]*(grams-1)
        for g1,g2 in zip(subgrams(c,grams),subgrams(c[1:],grams)):
            g1 = tuple(g1)
            g2 = tuple(g2)
            p += trans_table[g1][g2]

        p = -math.log(math.pow(2,p)+math.pow(2,-maxstrength),2) 
        res.append((c[grams-1:-(grams-1)],p))
    return res


if __name__ == "__main__":

    states=9 #four quadrants
    grams=3
    maxstrength=20
    train = None

    opts,args = getopt.getopt(sys.argv[1:], "s:n:m:ht:")
    for o,a in opts:
        if o == "-h":
            print USAGE
            exit(0)
        elif o == "-n":
            grams = int(a)
            continue
        elif o == "-s":
            states = int(a)
            continue
        elif o == "-m":
            maxstrength = int(a)
            continue
        elif o == "-t":
            train = a
            continue
        else:
            print "ERROR: unknown option '%s'"%(o)
            exit(1)

    
    training_codes = []
    for l in open(args[0] if not train else train):
        training_codes.append(map(int,l.strip()))

    codes = []
    for l in open(args[0]):
        codes.append(map(int,l.strip()))

    len_table = build_len_table(training_codes)
    trans_table = build_trans_table(training_codes,states,grams)
    start_table = build_start_table(training_codes)
    end_table = build_end_table(training_codes)

    #create a probalistic ranking of all codes
    res = strength(codes, grams, len_table, start_table, end_table, trans_table, maxstrength)
    res.sort(cmp=lambda a,b: cmp(a[1],b[1]))

    for c,p in res:
        print ".".join(map(str,c)), p

    probs = [p for c,p in res]

    # print "----"
    # print "mean:",np.mean(probs)
    # print "----"

    # print "min:",min(probs)
    # print "q1:",np.percentile(probs, 25)
    # print "median:",np.median(probs)
    # print "q3:",np.percentile(probs, 75)
    # print "max:",max(probs)
    
    print >> sys.stderr, " & ".join(("min","1q","med","mean","3q","max"))
    print >> sys.stderr, " & ".join(map(lambda x:"%0.2f"%x,(min(probs),np.percentile(probs, 25),np.median(probs),np.mean(probs),np.percentile(probs, 75),max(probs)))),"\\\\"
