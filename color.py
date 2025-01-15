


class TermColor:
    
    def __init__(self, code: str):
        self.code = code
        
    def __or__(self, tc):
        return TermColor(self.code + ";" + tc.code)
    
    def __str__(self):
        return "\033[" + self.code + "m"

    def __repr__(self):
        return "\033[" + self.code + "m"

RESET = TermColor("0")
BOLD = TermColor("1")
UNDERLINE = TermColor("4")
BLINK = TermColor("5")
RV = TermColor("7")

BLACK = TermColor("30")
RED = TermColor("31")
GREEN = TermColor("32")
YELLOW = TermColor("33")
BLUE = TermColor("34")
PURPLE = TermColor("35")
CYAN = TermColor("36")
WHITE = TermColor("37")


BBLACK = TermColor("40")
BRED = TermColor("41")
BGREEN = TermColor("42")
BYELLOW = TermColor("43")
BBLUE = TermColor("44")
BPURPLE = TermColor("45")
BCYAN = TermColor("46")
BWHITE = TermColor("47")


if __name__ == "__main__":
    print("Hello " + str(CYAN | BOLD) + "World!" + str(RESET))



