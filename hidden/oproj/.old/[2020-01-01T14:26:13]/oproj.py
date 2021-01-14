#!/usr/bin/env python3

import curses as curs
import os
import time
import sys
import math

proj_dir="/home/nyquist/Desktop/Projects/"

cmd_get_projects = \
f"""\
OLDIFS=$IFS
IFS=$'\n'
cd {proj_dir}
find . -maxdepth 1 -type l | sed 's/.\///g'
IFS=$OLDIFS
"""

LINES, COLS = os.popen('stty size', 'r').read().split()
projects    = os.popen(cmd_get_projects).read().split()

stdscr      = curs.initscr();
curs.curs_set(0)
curs.raw()
stdscr.keypad(True)
curs.noecho()
curs.cbreak()
stdscr.nodelay(True)

curs.start_color()
# curs.use_default_colors()
# curs.init_pair(1,7,-1)
# curs.init_pair(2,0,15)
# curs.init_pair(3,10,-1)

# curs.init_pair(1,7,0)
# curs.init_pair(2,0,2)
# curs.init_pair(3,10,0)

curs.init_pair(1,7,0)
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
lines_mid = math.floor(int(LINES)/2)
cols_mid = math.floor(int(COLS)/2)
title = "P-R-O-J-E-C-T-S"
# x = cols_mid - len(projects[0])
x = cols_mid - max(len(x) for x in projects)

while 1:
    key = stdscr.getch()

    # #debug
    # stdscr.addstr(0, 50, f"{select_idx}", curs.color_pair(1))

    # if key > 0:
    #     stdscr.addstr(0, 34, f"{key}", curs.color_pair(1))
    # #debug

    if key == key_q:
        break


    if key == key_moveup:
        select_idx = (select_idx + 1)%len(projects)
    if key == key_movedown:
        select_idx = (select_idx - 1)%len(projects)

    for idx, proj in enumerate(projects):
        y = lines_mid + idx

        stdscr.addstr(lines_mid-2, x-math.floor(len(title)/2)+10, title, curs.color_pair(3))

        if idx == select_idx:
            stdscr.addstr(y, x-math.floor(len(proj)/2)+10, proj, curs.color_pair(2))
        else:
            stdscr.addstr(y, x-math.floor(len(proj)/2)+10, proj, curs.color_pair(1))

        if key == key_v:
            cmd_selected = \
f"""\
urxvt -title "{projects[select_idx]}" -e sh -c "stty -ixon && cd {proj_dir}/{projects[select_idx]} && sudo vim; bash" 2> /dev/null &
"""
            os.system(cmd_selected)
            sys.exit()
        if key == key_d:
            cmd_selected = \
f"""\
urxvt -title "{projects[select_idx]}" -e sh -c "cd {proj_dir}/{projects[select_idx]} ; bash" 2> /dev/null &
"""
            os.system(cmd_selected)
            sys.exit()

        time.sleep(10 / 1000) # sleep for 50 milliseconds
curs.endwin()
