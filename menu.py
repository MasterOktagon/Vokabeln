import curses
from copy import *
import traceback

def menu(name: str, options: list[str]):
    try:
        selected = 0
        win = curses.initscr()
        curses.cbreak()
        curses.noecho()
        win.keypad(True)
        curses.curs_set(0)

        while True:
            win.clear()
            win.addstr(1, curses.COLS // 2 - len(name) // 2, name.upper(), curses.A_BOLD)

            for count in range(len(options)):
                s = copy(options[count])
                if selected == count: s = "[" + s + "]"
                win.addstr(5+count*2, curses.COLS//2-len(s)//2, s, (curses.A_BOLD | curses.A_UNDERLINE)*(selected==count))

            win.refresh()

            c = win.getch()
            if c == curses.KEY_UP:
                selected = max(selected - 1, 0)
                while options[selected] == "" and selected > 0:
                    selected = max(selected - 1, 0)

            if c == curses.KEY_DOWN:
                selected = min(selected + 1, len(options)-1)
                while options[selected] == "" and selected < len(options)-1:
                    selected = min(selected + 1, len(options)-1)

            if c == curses.KEY_ENTER or c == 10 or c == 13:
                curses.endwin()
                return options[selected]

    except Exception as err:
        curses.endwin()
        traceback.print_exc()


