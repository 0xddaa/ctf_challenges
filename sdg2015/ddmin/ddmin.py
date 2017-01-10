#!/usr/bin/env python
# $Id: ddmin.py,v 2.2 2005/05/12 22:01:18 zeller Exp $

from split import split
from listsets import listminus
from listsets import listintersect
import re
import subprocess as sp
import sys
import itertools

PASS       = "PASS"
FAIL       = "FAIL"
UNRESOLVED = "UNRESOLVED"

class Line:
    def __init__(self, no, code):
        line = dict()
        self.no = no
        self.code = code

def print_codes(codes):
    for c in codes:
        print c.code

def codes_to_input(codes):
    input = ""
    for c in codes:
        input += c.code + "\n"
    return input

def get_codes(text):
    codes = []
    for i, t in enumerate(text.split("\n")):
        l = Line(i, t)
        codes.append(l)
    return codes

def get_funcs():
    global codes

    funcs = dict()
    for l in codes:
        if "func" in l.code:
            name = re.search(" [\w]+\(", l.code).group()[1 : -1]
            funcs[name] = []
        elif "run" in l.code:
            name = "run"
            funcs[name] = []
        elif l.code == "":
            continue
        funcs[name].append(l)

    return funcs

def ddmin(c, test):
    def remove_funcs():
        for k in fs.keys():
            subset = codes_to_input(listminus(codes, fs[k]))
            if FAIL in test(subset, k):
                for l in fs[k]:
                    codes.remove(l)
                del fs[k]

    def remove_condition():
        for i in range(1, 10): # indent layer
            cond_codes = None
            for l in codes:
                if re.search("^\t{{{}}}(if|while)".format(i), l.code):
                    cond_codes = []
                    cond_codes.append(l)
                elif re.search("^\t{{{}}}".format(i+1), l.code):
                    if cond_codes != None:
                        cond_codes.append(l)
                else:
                    if cond_codes == None:
                        continue
                    subset = codes_to_input(listminus(codes, cond_codes))
                    if FAIL in test(subset, "if_" + str(cond_codes[0].no)):
                        for l in cond_codes:
                            codes.remove(l)
                    cond_codes = None

            
            
        

    def trace(cf, traced):
        def line_has_func(line, traced):
            for k in fs.keys():
                if k in line.code and cf != k and not traced[k]:
                    nfs.append(k)
    
        traced[cf] = True
        for line in reversed(fs[cf]):
            subset = codes_to_input(listminus(codes, [line]))
            if FAIL in test(subset, line.no):
                codes.remove(line)
            else:
                line_has_func(line, traced)

        return traced 

    # init 
    global codes, fs, nfs
    codes = get_codes(c) # codes, list
    fs = get_funcs() # functions, dict
    cf = None # current function

    remove_funcs()
    remove_condition()
    fs = get_funcs() # update functions

    traced = dict() # traced functions
    for k in fs.keys():
        traced[k] = False

    nfs = [] # functions in current text
    nfs.append("run")
    while len(nfs) > 0:
        cf = nfs.pop(0)
        traced = trace(cf, traced)

    # remove unused code
    for k in traced.keys():
        if traced[k] == True:
            continue
        for line in fs[k]:
            codes.remove(line)

    return codes_to_input(codes)

if __name__ == "__main__":
    tests = {}
    circumstances = []
    
    def mytest(c, index):
        global tests
        global circumstances

        open("/tmp/sub_c", "w").write(c)
        cmd = sys.argv[1] + " < " + "/tmp/sub_c"
        err = sp.call(cmd, shell = True, stdout = sp.PIPE, stderr = sp.PIPE)
        p = sp.Popen(cmd, shell = True, stdout = sp.PIPE, stderr = sp.PIPE)

        if "Syntax Error" in p.stdout.read():
            tests[index] = UNRESOLVED
            return UNRESOLVED
        elif err == 0 or err == 1:
            tests[index] = PASS
            return PASS
        else:
            tests[index] = FAIL
            return FAIL


    circumstances = open(sys.argv[2], "r").read().split("\n")
    c = ""
    for cmd in circumstances:
        if cmd != "":
            c += cmd + "\n"

    c2 = ""
    while True:
        c2 = ddmin(c, mytest)
        if c2.strip("\n") == c.strip("\n"):
            break
        else:
            c = c2

    print c.strip("\n")
