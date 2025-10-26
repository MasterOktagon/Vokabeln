import curses
from copy import *
import traceback
import os

import checker
import manager
import menu
import random
from i18 import i18n
import getstr

import json

def rmenu() -> list[str]|int:
    try:
        selected: int = 0
        selection: list[int] = []
        win = curses.initscr()
        curses.cbreak()
        curses.noecho()
        win.keypad(True)
        curses.curs_set(0)

        name = i18n("Choose set")

        options: list[str] = []
        opt_info: list[str] = []
        opt_path: list[str] = []
        for dir_path, _dir_names, filenames in os.walk(r"./sets/"):
            for file in filenames:
                options.append(file)

                info = dir_path
                opt_path.append(dir_path)
                info += "\n\n" + str(len(manager.load_set(info + "/" + file))) + " " + i18n("Vocabulars")

                opt_info.append(info)

        options += ["", "", i18n("OK"), i18n("Abort")]
        opt_info += ["","","", ""]
        opt_path += ["", "", "", ""]

        subwin = win.subwin(4, curses.COLS // 2 - 1)

        while True:
            win.clear()
            subwin.clear()
            subwin.border()
            win.addstr(1, curses.COLS // 2 - len(name) // 2, name.upper(), curses.A_BOLD)

            last_dir = ""
            winlen = -1

            for count in range(len(options)):

                if opt_path[count] != last_dir and opt_path[count] != "":
                    pre = "> "
                    is_selected = sum([opt_path[f]==opt_path[count] for f in selection])
                    if opt_path[count] == opt_path[selected]: pre = "v "
                    win.addstr(5 + (winlen := winlen+1), 2, pre + opt_path[count][7:], curses.A_UNDERLINE*bool(is_selected))
                    last_dir = opt_path[count]
                if options[count] in ["",i18n("Abort"),i18n("OK")] or opt_path[selected] == opt_path[count]:
                    s = copy(options[count])
                    if "." in s: s = s[:s.rfind(".")]
                    if selected == count: s = "[" + s + "]"
                    win.addstr(5+(winlen := winlen+1), 4 + (selected != count), s, (curses.A_BOLD | curses.A_UNDERLINE)*(selected==count) | (curses.A_UNDERLINE)*(count in selection))
                    if selected == count and not (options[count] in [i18n("Abort"),i18n("OK")]): subwin.addstr(0,1, s, curses.A_BOLD)
                    for c,s in enumerate(opt_info[selected].split("\n")):
                        subwin.addstr(c+2,1,s)

            #curses.resize_term()
            win.refresh()

            c = win.getch()
            if c == curses.KEY_UP:
                selected = max(selected - 1, 0)
                while options[selected] == "" and selected > 0:
                    selected = max(selected - 1, 0)

            elif c == curses.KEY_DOWN:
                selected = min(selected + 1, len(options)-1)
                while options[selected] == "" and selected < len(options)-1:
                    selected = min(selected + 1, len(options)-1)

            elif c == curses.KEY_ENTER or c == 10 or c == 13:

                if options[selected] == i18n("OK"):
                    curses.endwin()
                    out: list[str] = []
                    for i in selection:
                        out.append(opt_info[i][:opt_info[i].find("\n")] + "/" + options[i])

                    return out

                if options[selected] == i18n("Abort"):
                    curses.endwin()
                    return 0

                if selected in selection:
                    selection.remove(selected)
                else:
                    selection.append(selected)

    except Exception:
        curses.endwin()
        traceback.print_exc()

def req(sets: list[str]) -> None:
    if not sets: return
    print(sets)

    lang = sets[0][sets[0].find("/",6)+1 : sets[0].find("/",sets[0].find("/",6)+1)]
    print(lang)

    select_mod = ""
    if (select_mod := menu.menu(i18n("Choose mode"), [i18n("English-{0}").format(lang),i18n("{0}-English").format(lang),i18n("Random"),"",i18n("Abort")])) == i18n("Abort"):
        return

    print(i18n("Mode")+":",select_mod)

    data = {}
    for s in sets:
        data.update(manager.load_set(s))

    pairs: list[list[str]] = []
    if i18n("English-") in select_mod:
        pairs = [[d, data[d]] for d in data.keys()]
    elif i18n("-English") in select_mod:
        pairs = [[data[d], d] for d in data.keys()]
    else:
        for d in data.keys():
            if random.randint(0, 1) == 0:
                pairs.append([d, data[d]])
            else:
                pairs.append([data[d], d])

    try:
        win = curses.initscr()
        curses.cbreak()
        win.keypad(True)
        curses.curs_set(1)
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, -1, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_RED, -1)
        curses.init_pair(2, curses.COLOR_GREEN, -1)
        curses.init_pair(4, 6, -1)
        curses.init_pair(19, -1, 233)

        for i in range(21):
            curses.init_pair(19+i, -1, 233+i)

        correct = 0
        i = 0
        wrong = []
        begin = True
        name = ""
        sets.sort()
        for s in sets:
            name += s[s.rfind("/")+1:s.rfind(".")] + "+"
        name = name[:-1]
        while wrong != [] or begin:
            begin = False
            wrong = []
            while pairs:
                win.clear()
                this = pairs.pop(random.randint(0, len(pairs) - 1))

                win.clear()
                title = i18n("Checking: {0} ({1}/{2})").format(name, i+1, len(data))
                win.addstr(1, curses.COLS // 2 - len(title) // 2, title[:min(curses.COLS - len(title)//2, len(title))], curses.A_BOLD)
                win.addstr(3, 5, this[0])
                win.addstr(5, 5, ">>> ")
                curses.setsyx(5,9)

                win.refresh()
                curses.echo()
                inp = getstr.getstr(5,9, win)
                curses.noecho()
                if inp == "<exit>":
                    curses.endwin()
                    return

                if inp == this[1] or inp in this[1].split("/"):
                    win.addstr(6,5, i18n("CORRECT!"), curses.color_pair(2) | curses.A_BOLD)
                    correct += 1

                else:
                    wrong.append(this)
                    correct -= 1

                    try:
                        col = False
                        j = 0
                        for c in checker.visualize_v2(this[1], inp)[0]:
                            if c == "$": col = not col
                            else:
                                win.addch(6, 9+j, c, (curses.color_pair(1))*col)
                                j += 1
                    except KeyboardInterrupt:
                        win.addstr(6, 9, this[1], curses.color_pair(1))
                    win.addstr(7, 9, i18n("WRONG!"), curses.color_pair(3) | curses.A_BOLD)

                if getstr.wait(win) != "":
                    curses.endwin()
                    return

                #win.addstr(9, 5, i18n("Input any to continue. input 'q' to abort: "))
                #win.refresh()
                #while not(sel := win.getch()): pass
                #if sel == ord("q"):
                #    curses.endwin()
                #    return

                i += 1

            pairs = wrong.copy()

        win.clear()
        curses.curs_set(0)

        caption = i18n("Evaluation: - {0}").format(name)
        win.addstr(1, curses.COLS // 2 - len(caption) // 2,caption, curses.A_BOLD)
        win.addstr(3, 5, i18n("SCORE:") + f" {max(correct, 0)}/{len(data)}", curses.A_BOLD)
        win.addstr(4, 13, f"{round(max(correct, 0)/len(data)*100, 1)}%", curses.A_BOLD)

        with open("meta/scores.json", "r") as f:
            scores = json.loads(f.read())

        if not(name in scores.keys()):
            scores[name] = [max(correct, 0)/len(data)]
        else:
            if(len(scores[name]) > 9): scores[name].pop(0)
            scores[name].append(max(correct, 0)/len(data))

        sw = win.subwin(23,42,10,5)

        graph(sw, scores[name])

        curses.noecho()
        c = 0
        while not(c == curses.KEY_ENTER or c == 10 or c == 13): c = win.getch()

        with open("meta/scores.json", "w") as f:
            f.write(json.dumps(scores))

        curses.endwin()
    except Exception:
        curses.endwin()
        traceback.print_exc()


def graph(win, scores):
    try:
        win.border()
        for c,s in enumerate(scores[:20]):
            win.addstr(20-int(20*s)+1, c*4+1, "    ", curses.A_REVERSE)
            for i in range(20-int(20*s)+2, 22, 1):
                win.addstr(i, c * 4 + 1, " ", curses.color_pair(39 - i) | curses.A_REVERSE*(i<=20-int(20*scores[max(c-1,0)])+1))
                win.addstr(i, c * 4 + 2, "  ", curses.color_pair(39 - i))
                win.addstr(i, c * 4 + 4, " ", curses.color_pair(39 - i) | curses.A_REVERSE*(i<=20-int(20*scores[min(c+1,len(scores)-1)])+1))
    except curses.error:
        win.addstr(1,1, "ERROR " + str(curses.ERR))
