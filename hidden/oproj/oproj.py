#!/usr/bin/env python3

import curses as curs
import os
import sys
import math
from window import *

win = Window()

proj_dir = "/home/nyquist/Desktop/Projects"

cmd_get_projects = \
f"""\
OLDIFS=$IFS
IFS=$'\/n'
cd {proj_dir}
find . -maxdepth 1 -type l | sed 's/.\///g'
IFS=$OLDIFS
"""
cmd_get_branch = \
f"""\
OLDIFS=$IFS
IFS=$'\/n'
cd {proj_dir}
find . -maxdepth 1 -type l | sed 's/.\///g'
IFS=$OLDIFS
"""

LINES, COLS = os.popen('stty size', 'r').read().split()
LINES = int(LINES)
COLS = int(COLS)

curs.start_color()
curs.use_default_colors()
curs.init_pair(1, 7, -1)
curs.init_pair(2, 0, 3)
curs.init_pair(3, 3, -1)

select_idx = 0
key = 0
key_moveup = 106
key_movedown = 107
key_enter = 10
key_q = 113
key_v = 118
key_d = 100
key_u = 117
key_e = 101

lines_mid = math.floor(LINES/2)
title = "P-R-O-J-E-C-T-S"

def move(dire, num, wrap):
    wrapLen = len(wrap)
    if dire == 'up':
        num = (num + 1)%wrapLen
    elif dire == 'down':
        num = (num - 1)%wrapLen
    return num


def select(selected, cords, string):
    if selected:
        win.scr.addstr(cords[0], cords[1], string, curs.color_pair(2))
    else:
        win.scr.addstr(cords[0], cords[1], string, curs.color_pair(1))


cmd_selected = "xclip <<< 'echo exited'"

cords = [0, 0]

def getProjects():
    return os.popen(cmd_get_projects).read().split()

while 1:
    projects = getProjects()
    run = len(projects) > 0

    if not run:
        cmd_selected = "xclip <<< 'echo no projects'"
        break

    cords[1] = math.floor(COLS/2)-math.floor(len(title)/2)
    # selected_x = x+2
    key = win.scr.getch()

    # #debug
    # win.scr.addstr(0, 50, f"{select_idx}", curs.color_pair(1))

    # if key > 0:
    #     win.scr.addstr(0, 34, f"{key}", curs.color_pair(1))
    # #debug

    if key == key_q:
        break

    if key == key_moveup:
        select_idx = move('up', select_idx, projects)

    elif key == key_movedown:
        select_idx = move('down', select_idx, projects)

    elif key == key_enter:
        cmd_selected = \
f"""\
xclip <<< "cd $(readlink -f {proj_dir}/{projects[select_idx]})"
"""
        break
    elif key == key_u:
        cmd = f"sudo rm -R {proj_dir}/{projects[select_idx]}"

        os.system(cmd)
        win.scr.clear()

        if select_idx != 0:
            select_idx -= 1
        continue

    for idx, proj in enumerate(projects):
        cords[0] = lines_mid + idx

        win.scr.addstr(lines_mid-2, cords[1], title, curs.color_pair(3))

        select(idx == select_idx, cords, proj)

    win.scr.refresh()

os.system(cmd_selected)
curs.endwin()
sys.exit()
