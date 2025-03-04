import json

lang = "english"
intz = {}

def load(l: str)->str:
    global lang, intz
    lang = l
    if lang != "english":
        with open("./meta/lang/" + lang + ".json", "r") as f:
            print("lang loaded!")
            intz = json.loads(f.read())

def i18n(s: str)->str:
    global lang, intz
    if lang == "english": return s
    try:
        return intz[s]
    except KeyError:
        return s


