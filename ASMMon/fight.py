#!/usr/bin/python2.7

import sys
import argparse
import re
import time
import os 
from ASMMon import ASMMon

s = ASMMon()
e = ASMMon()

args = None

def check_fmt(act):
    pat = "^ *("
    # legal instructions
    for ins in ["mov", "int", "cmp", "jmp", "je", "ja", "jne", "add", "sub", "mod"]:
        pat += ins + "|"
    pat = pat[:-1]
    pat += ") +(e[abcd]x|e[sd]i|0x80|[\d]+)( *$| *, *(e[abcd]x|e[sd]i|[\d]+) *$)"
    return re.search(pat, act)

def check_logic(act):
    if re.search("^ *mov", act):
        return re.search("^ *mov +e[abcd]x*?", act)
    elif re.search("^ *(jmp|je|ja|jne)", act):
        return re.search("^ *(jmp|je|ja|jne) +[\d]+ *$", act)
    elif re.search("^ *int*?", act):
        return re.search(" *int +0x80 *$", act)
    elif re.search("^ *cmp*?", act):
        return True 
    elif re.search("^ *(add|sub|mod)*?", act):
        return re.search("^ *(add|sub|mod) +e[abcd]x*?", act)
    else:
        return False

def parse_actions(acts):
    for act in acts:
        if not check_fmt(act) or not check_logic(act):
            print "Instruction \"{}\" illegal".format(act)
            return False
        
    return True

def log_info(info):
    os.system("echo \"{}\" >> {}".format(info, args.log))

def start_game():
    s.eip = 1
    e.eip = 1
    s.set_name("Ash Ketchum")
    e.set_name("Gary Oak")

    stime = int(time.time())

    while True:
        if int(time.time()) - stime > args.time:
            print "Time's up!"
            break
        if s.no_hp() or e.no_hp():
            break
        if s.no_ins() or e.no_ins():
            break

        act = s.acts[s.eip - 1]
        s.ni(e)
        log_info(s.print_info(e, act))
        act = e.acts[e.eip - 1]
        e.ni(s)
        log_info(e.print_info(s, act))

def main():
    global args

    parser = argparse.ArgumentParser(description='ASM battle')
    parser.add_argument("-e", "--enemy", help="Enemy's actions.", default="enemy", required = True, metavar = "ENEMY ACTION")
    parser.add_argument("-s", "--self", help="Your's actions.", default="self", required = True, metavar = "SELF ACTION")
    parser.add_argument("-i", "--info", help="Show the battle info.", action='store_true')
    parser.add_argument("--log", help="Battle log", default="/tmp/log_" + str(os.getpid()), metavar = "PATH")
    parser.add_argument("-t", "--time", type=int, help="Fight time.", default=10)
    args = parser.parse_args()
    
    os.system("echo > " + args.log)

    try:
        self_acts = open(args.self, "r").read().strip().split("\n")
        enemy_acts = open(args.enemy, "r").read().strip().split("\n")
    except:
        print "File not found!"
        sys.exit(0)
    
    if parse_actions(self_acts):
        s.set_actions(self_acts)
        s.is_legal = True
    if parse_actions(enemy_acts):
        e.set_actions(enemy_acts)
        e.is_legal = True

    start_game()
    
    # judge winner, 0 = self, 1 = enemy
    if (s.is_legal and e.is_legal) or \
        (not s.is_legal and not e.is_legal): # judge by HP
        if s.esi == e.esi:
            winner = 1
        else:
            winner = 0 if s.esi > e.esi else 1
    else: # judge by legal
        winner = 0 if s.is_legal else 1

    if winner == 0:
        print "Ash Ketchum win!"
        log_info("Ash Ketchum win!")
        print open("/home/ASMMon/flag", "r").read()
    else:
        print "Gary Oak win!"
        log_info("Gary Oak win!")
        
main()
