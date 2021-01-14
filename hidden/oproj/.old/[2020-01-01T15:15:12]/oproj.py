#!/usr/bin/env python3

import curses as curs
import os
import time
import sys
import math

proj_dir="/home/nyquist/Desktop/Projects"

cmd_get_projects = \
f"""\
OLDIFS=$IFS
IFS=$'\n'
cd {proj_dir}
find . -maxdepth 1 -type l | sed 's/.\///g'
IFS=$OLDIFS
"""

LINES, COLS = os.popen('stty size', 'r').read().split()
LINES = int(LINES)
COLS  = int(COLS)

stdscr = curs.initscr();
curs.curs_set(0)
curs.raw()
stdscr.keypad(True)
curs.noecho()
curs.cbreak()
stdscr.nodelay(True)

curs.start_color()
curs.use_default_colors()
curs.init_pair(1,7,-1)
curs.init_pair(2,0,3)
curs.init_pair(3,3,0)

select_idx = 0
key = 0
key_moveup = 106
key_movedown = 107
key_enter = 10
key_q = 113
key_v = 118
key_d = 100
key_u = 117

lines_mid = math.floor(LINES/2)
title = "P-R-O-J-E-C-T-S"

def centerText(text):
    math.floor(COLS/2)-math.floor(len(text)/2)

cmd_selected = f"xclip <<< 'echo exited'"

while 1:

    projects = os.popen(cmd_get_projects).read().split()
    run = len(projects) > 0

    if not run:
        cmd_selected = f"xclip <<< 'echo no projects'"
        break

    x = math.floor(COLS/2)
    key = stdscr.getch()

    # #debug
    # stdscr.addstr(0, 50, f"{select_idx}", curs.color_pair(1))

    # if key > 0:
    #     stdscr.addstr(0, 34, f"{key}", curs.color_pair(1))
    # #debug

    if key == key_q:
        break
    elif key == key_moveup:
        select_idx = (select_idx + 1)%len(projects)
    elif key == key_movedown:
        select_idx = (select_idx - 1)%len(projects)
    elif key == key_v:
        cmd_selected = \
f"""\
xclip <<< "cd {proj_dir}/{projects[select_idx]} && sudo vim"
"""
        break
    elif key == key_d:
        cmd_selected = \
f"""\
xclip <<< "cd {proj_dir}/{projects[select_idx]}"
"""
        break

    for idx, proj in enumerate(projects):
        y = lines_mid + idx

        stdscr.addstr(lines_mid-2, x-math.floor(len(title)/2), title, curs.color_pair(3))

        if idx == select_idx:
            stdscr.addstr(y, x-math.floor(len(proj)/2), proj, curs.color_pair(2))
        else:
            stdscr.addstr(y, x-math.floor(len(proj)/2), proj, curs.color_pair(1))


        time.sleep(10 / 1000) # sleep for 50 milliseconds
os.system(cmd_selected)
curs.endwin()
sys.exit()
