import curses
import locale
from i18 import i18n

locale.setlocale(locale.LC_ALL, "")

def getstr(y: int, x: int, win: curses.window, instr="", suffix="")->str:
    cursor = len(instr)
    curses.noecho()
    sel_start = cursor

    def redraw(trail: int=0):
        #win.addstr(y+2, x, "c: "+str(cursor))
        #win.addstr(y+3, x, "s: "+str(sel_start))
        if sel_start == cursor:
            win.addstr(y,x, instr)
            win.addstr(y,x+len(instr), suffix + " "*trail, curses.color_pair(4))
            win.addstr(y,x, instr[:cursor])

        else:
            if sel_start < cursor:
                win.addstr(y,x, instr)
                win.addstr(y,x+len(instr), suffix + " "*trail, curses.color_pair(4))
                win.addstr(y,x, instr[:sel_start])
                win.addstr(y,x+sel_start, instr[sel_start:cursor], curses.A_REVERSE)
            else:
                win.addstr(y,x, instr[:sel_start], curses.A_REVERSE)
                win.addstr(y,x+sel_start, instr[sel_start:])
                win.addstr(y,x+len(instr), suffix + " "*trail, curses.color_pair(4))
                win.addstr(y,x, instr[:cursor])


    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(3, curses.COLOR_RED, -1)
    curses.init_pair(4, 4, -1)

    redraw()

    while True:
        try:
            c: str = win.get_wch()
        except curses.error as e:
            win.clear()
            redraw()
            win.addstr(y+2, x+5, "curses error occured: " + repr(e), curses.color_pair(3))
            continue

        if isinstance(c, int):
            if c == curses.KEY_LEFT:
                cursor = max(cursor-1, 0)
                sel_start = cursor
                redraw()

            elif c == curses.KEY_RIGHT:
                cursor = min(cursor+1, len(instr))
                sel_start = cursor
                redraw()

            elif c == curses.KEY_SLEFT:
                cursor = max(cursor-1, 0)
                redraw()

            elif c == curses.KEY_SRIGHT:
                cursor = min(cursor+1, len(instr))
                redraw()
            
            elif c == curses.KEY_BACKSPACE:
                if cursor != sel_start:
                    instr = instr[:min(sel_start, cursor)] + instr[max(sel_start, cursor):]
                    a = abs(sel_start - cursor)
                    cursor = min(cursor, sel_start)
                    sel_start = cursor
                    redraw(a)
                elif cursor > 0:
                    instr = instr[:cursor - 1] + instr[cursor:]
                    cursor -= 1
                    sel_start = cursor
                    redraw(1)
            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                break

            elif c == curses.KEY_DC:
                if cursor != sel_start:
                    instr = instr[:min(sel_start, cursor)] + instr[max(sel_start, cursor):]
                    a = abs(sel_start - cursor)
                    cursor = min(cursor, sel_start)
                    sel_start = cursor
                    redraw(a)
                elif cursor < len(instr):
                    instr = instr[:cursor] + instr[cursor+1:]
                    sel_start = cursor
                    redraw(1)

        else:
            if c == '\n':
                break

            elif c == '\x1b': # ESC
                win.addstr(y, x, i18n("Abort") + "...", curses.color_pair(3))
                curses.echo()
                return "<exit>"

            else:
                if cursor != sel_start:
                    instr = instr[:min(sel_start, cursor)] + instr[max(sel_start, cursor):]
                    a = abs(sel_start - cursor)
                    cursor = min(cursor, sel_start)
                    sel_start = cursor
                    redraw(a)
                instr = instr[:cursor] + c + instr[cursor:]
                cursor += len(c)
                sel_start = cursor
                redraw()

    curses.echo()
    return instr

def wait(win: curses.window):
    while True:
        try:
            c: str = win.get_wch()
        except curses.error as e:

            win.addstr(6, 5, "curses error occured: " + repr(e), curses.color_pair(2))
            continue

        if isinstance(c, int):
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                return ""

        else:
            #print(c, " % ", hex(ord(c)))
            if c == '\n':
                return ""

            elif c == '\x1b': # ESC
                curses.echo()
                return "<exit>"