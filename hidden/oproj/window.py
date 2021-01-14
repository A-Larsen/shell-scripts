#!/usr/bin/env python3
import curses as curs
import math
import os
LINES, COLS = os.popen('stty size', 'r').read().split()

# we can debug this module by running it with python interpreture
# $ python
# >>> from window import *

def center_text(text:str, offsety:int=0, offsetx:int=0)->object:
    class cords:
        pass

    cords.y = \
    math.floor(curs.LINES/2) + offsety

    cords.x = \
    math.floor(curs.COLS/2) - math.floor(len(text)/2) + offsetx

    return cords

class Window:
    def __init__(self)->None:
        "add all curses predifined variables"
        self.scr = curs.initscr()
        self.nodelay = True
        self.scr.nodelay(self.nodelay)
        self.scr.keypad(True)
        curs.LINES = int(LINES)
        curs.COLS = int(COLS)
        curs.noecho()
        curs.cbreak()
        curs.curs_set(0)

    def input(self, y:int, x:int)->(str, int):
        "get user input"
        stringPos = -1
        string = ""

        while True:
            self.scr.nodelay(False)
            ch = self.scr.getch()
            string += chr(ch)
            if ch == 265: # f1
                return 0

            if ch == 10: # enter
                self.scr.nodelay(self.nodelay)
                return string.rstrip() # removing eol "\n"
            else:
                self.scr.addstr(y, x, string)

class Word(Window):
    def __init__(self, Window:object, word:str)->None:
        "get word and set position"
        cords = center_text(word)
        self.y = cords.y
        self.x = cords.x
        self.string = word
        Window.scr.addstr(self.y, self.x, self.string)
