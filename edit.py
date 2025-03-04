import curses
import traceback
import manager
import os
from copy import *
import math
import time

import menu

def new_set_menu(error = "") -> str|int:
    try:
        win = curses.initscr()
        curses.cbreak()
        curses.noecho()
        win.keypad(True)
        curses.curs_set(0)
        
        name = "Satznamen wählen"
        while True:
            win.clear()
            win.addstr(1, curses.COLS // 2 - len(name) // 2, name.upper(), curses.A_BOLD)
            win.addstr(4, 1, "Satzname (leer bricht ab, '/' markiert unterordner):")
            win.addstr(5, 4, error)
            win.addstr(6, 5, ">>> ")
            curses.echo()
            curses.curs_set(1)
            try: inp = win.getstr(6, 9).decode("utf-8")
            except UnicodeDecodeError: continue
            curses.noecho()
            curses.curs_set(0)

            if inp == "": return 0
            if inp.count("/") < 1:  return new_set_menu(f"FEHLER: Satz {inp} ist in keinem Sprachunterordner")
            inp = "sets/" + inp
            inp += ".json"
            
            if os.path.isfile(inp): return new_set_menu(f"FEHLER: Satz {inp} existiert bereits!")
            with open(inp, "w") as f:
                f.write("{}")
            return inp
        
    except:
        return 0


def rmenu() -> str|int:
    try:
        selected: int = 0
        selection: list[int] = []
        win = curses.initscr()
        curses.cbreak()
        curses.noecho()
        win.keypad(True)
        curses.curs_set(0)

        name = "Satz wählen (Bearbeitung)"

        options: list[str] = []
        opt_info: list[str] = []
        opt_path: list[str] = []
        for dir_path, _dir_names, filenames in os.walk(r"./sets/"):
            for file in filenames:
                options.append(file)

                info = dir_path
                opt_path.append(dir_path)
                data = manager.load_set(info + "/" + file)
                info += "\n\n" + str(len(data)) + " Vokabeln\n\n"
                for k in data.keys():
                    info += k + ": " + data[k] +"\n"

                opt_info.append(info)

        options += ["", "", "Neu", "Abbruch"]
        opt_info += ["", "", "Erstelle einen neuen Satz", ""]
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
                    is_selected = sum([opt_path[f] == opt_path[count] for f in selection])
                    if opt_path[count] == opt_path[selected]: pre = "v "
                    win.addstr(5 + (winlen := winlen + 1), 2, pre + opt_path[count][7:],
                               curses.A_UNDERLINE * bool(is_selected))
                    last_dir = opt_path[count]
                if options[count] in ["", "Neu", "Abbruch", "OK"] or opt_path[selected] == opt_path[count]:
                    s = copy(options[count])
                    if "." in s: s = s[:s.rfind(".")]
                    if selected == count: s = "[" + s + "]"
                    win.addstr(5 + (winlen := winlen + 1), 4 + (selected != count), s,
                               (curses.A_BOLD | curses.A_UNDERLINE) * (selected == count) | (curses.A_UNDERLINE) * (
                                           count in selection))
                    if selected == count and not (options[count] in ["Abbruch", "OK"]): subwin.addstr(0, 1, s,
                                                                                                      curses.A_BOLD)

                    overflow = math.inf
                    for c, s in enumerate(opt_info[selected].split("\n")):
                        if c+10 < curses.LINES: subwin.addstr(c + 2, 1, s)
                        else: overflow = min(c, overflow)

                    if overflow != math.inf: subwin.addstr(overflow+2, 1, "  ...")

            # curses.resize_term()
            win.refresh()

            c = win.getch()
            if c == curses.KEY_UP:
                selected = max(selected - 1, 0)
                while options[selected] == "" and selected > 0:
                    selected = max(selected - 1, 0)

            elif c == curses.KEY_DOWN:
                selected = min(selected + 1, len(options) - 1)
                while options[selected] == "" and selected < len(options) - 1:
                    selected = min(selected + 1, len(options) - 1)

            elif c == curses.KEY_ENTER or c == 10 or c == 13:

                if options[selected] == "Abbruch":
                    curses.endwin()
                    return 0
                elif options[selected] == "Neu":
                    curses.endwin()
                    return new_set_menu()
                return opt_path[selected] + "/" + options[selected]

    except Exception:
        curses.endwin()
        traceback.print_exc()


def set_menu(s: str):
    data = manager.load_set(s)

    name = "Satz bearbeiten - " + s
    lang = s[s.find("/", 6) + 1: s.find("/", s.find("/", 6) + 1)]

    try:
        win = curses.initscr()
        curses.cbreak()
        curses.noecho()
        win.keypad(True)
        curses.curs_set(0)

        subwin = win.subwin(6, 0)

        selected = 0
        opt_selected = 1

        options = ["Tauschen", "Speichern", "Schließen"]
        saved = True

        while True:
            win.clear()
            subwin.clear()
            win.addstr(1, curses.COLS // 2 - len(name) // 2, name.upper(), curses.A_BOLD)
            subwin.border()
            subwin.addstr(0,1, "[Deutsch]", curses.A_BOLD)
            subwin.addstr(0,curses.COLS//2, f"[{lang}]", curses.A_BOLD)

            for count, opt in enumerate(options):
                if opt == "Speichern" and not saved: opt = "Speichern*"
                if opt_selected == count:
                    win.addstr(3, curses.COLS//(len(options)+1)*(count+1)-(len(opt)+2)//2, f"[{opt}]", curses.A_BOLD | curses.A_UNDERLINE)
                else:
                    win.addstr(3, curses.COLS // (len(options) + 1) * (count + 1) - (len(opt) + 2) // 2, f" {opt} ")

            curline = 0
            if len(data) > 0:
                list_end = min(len(data), max(selected + (curses.LINES - 11) // 2, curses.LINES - 11))
                list_begin = max(0, min(selected-(curses.LINES-10)//2, len(data)-(curses.LINES-11)))
                if list_begin != 0:
                    subwin.addstr(1,1, " ...")
                    subwin.addstr(1,curses.COLS//2, " ...")
                if list_end != len(data):
                    subwin.addstr(curses.LINES-8, 1, " ...")
                    subwin.addstr(curses.LINES-8, curses.COLS//2, " ...")
                for i in range(list_begin, list_end,1):
                    key = list(data.keys())[i]
                    subwin.addstr(curline + 2, 1, key + " "*(curses.COLS//2+1-len(key)), (curses.A_REVERSE | curses.A_BOLD) * (selected == i))
                    subwin.addstr(curline + 2, curses.COLS//2, data[key] + " "*(curses.COLS//2-len(data[key])-1), (curses.A_REVERSE | curses.A_BOLD) * (selected == i))

                    if i == selected:
                        l = "└   [+] Hinzufügen     [#] Bearbeiten    [-] Löschen"
                        subwin.addstr(curline + 3, 1, l+" "*(curses.COLS-2-len(l)), curses.A_REVERSE)
                        curline += 1

                    curline += 1

            else:
                l = "    [+] Hinzufügen"
                subwin.addstr(curline + 3, 1, l + " " * (curses.COLS - 2 - len(l)), curses.A_REVERSE)

            win.refresh()

            c = win.getch()
            if c == curses.KEY_UP:
                selected = max(selected-1, 0)
            elif c == curses.KEY_DOWN:
                selected = min(selected+1, len(data)-1)
            elif c == curses.KEY_LEFT:
                opt_selected = max(opt_selected-1, 0)
            elif c == curses.KEY_RIGHT:
                opt_selected = min(opt_selected+1, len(options)-1)
            elif c == ord("-") and len(data) > 0:
                del data[list(data.keys())[selected]]
                saved = False
            elif c == ord("+"):
                while True:
                    subwin.clear()
                    win.clear()

                    name2 = "Neues Paar"
                    win.addstr(1, curses.COLS // 2 - len(name2) // 2, name2.upper(), curses.A_BOLD)

                    win.addstr(3, 5, "Worte eingeben (leer bricht ab, '|' zwischen die Sprachen): ")
                    win.addstr(5, 5, ">>> ")
                    curses.setsyx(5, 9)

                    win.refresh()
                    curses.echo()
                    curses.curs_set(1)
                    try: inp = win.getstr(5, 9).decode("utf-8")
                    except UnicodeDecodeError: continue
                    curses.noecho()
                    curses.curs_set(0)

                    if inp == "": break
                    try:
                        m = inp.split("|")
                        data[m[0]] = m[1]

                    except IndexError:
                        win.addstr(7,5,"Nur eine Sprache wurde eingegeben. verwende '|' zwischen den Sprachen!")
                        win.refresh()
                        time.sleep(1)

                    saved = False

            elif c == ord("#") and len(data) > 0:
                sel_key = list(data.keys())[selected]
                sel_data = data[sel_key]
                while True:
                    subwin.clear()
                    win.clear()

                    name2 = "Paar bearbeiten"
                    win.addstr(1, curses.COLS // 2 - len(name2) // 2, name2.upper(), curses.A_BOLD)

                    win.addstr(3, 5, "Worte eingeben (leer bricht ab, '|' zwischen die Sprachen): ")
                    win.addstr(5, 5, ">>> " + sel_key + "|" + sel_data)
                    curses.setsyx(5, 9)

                    win.refresh()
                    curses.echo()
                    curses.curs_set(1)
                    try: inp = win.getstr(5, 9).decode("utf-8")
                    except UnicodeDecodeError: continue
                    curses.noecho()
                    curses.curs_set(0)

                    if inp == "": break
                    try:
                        m = inp.split("|")
                        del data[sel_key]
                        data[m[0]] = m[1]

                    except IndexError:
                        win.addstr(7,5,"Nur eine Sprache wurde eingegeben. verwende '|' zwischen den Sprachen!")
                        win.refresh()
                        time.sleep(1)
                        continue

                    saved = False
                    break

            elif c == curses.KEY_ENTER or c == 10 or c == 13:
                if options[opt_selected] == "Schließen":
                    if not saved:
                        if(menu.menu("Ungespeicherte Änderungen!", ["Abbruch", "Schließen"]) == "Schließen"):
                            curses.endwin()
                            return
                    else:
                        curses.endwin()
                        return
                if options[opt_selected] == "Speichern":
                    manager.save_set(s, data)
                    saved = True

                elif options[opt_selected] == "Tauschen" and len(data) > 0:
                    sel_key = list(data.keys())[selected]
                    sel_v   = data[sel_key]
                    del data[sel_key]
                    data[sel_v] = sel_key

                    saved = False




    except Exception:
        curses.endwin()
        traceback.print_exc()

