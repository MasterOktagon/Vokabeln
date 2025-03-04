import color
import menu
import req
import edit
import i18
import json
from i18 import i18n

with open("./meta/settings.json", "r") as f:
    settings = json.loads(f.read())
    i18.load(settings["language"])
    print(f"The chosen language is: {settings['language']}")

while (selection := menu.menu(i18n("Vokabelprogramm - CUI v2"), [i18n("Check vocabulary"), i18n("Edit vocabulary"), "", i18n("Quit")])) != i18n("Quit"):
    if selection == i18n("Check vocabulary"):
        if (selection_req := req.rmenu()) != 0:
            req.req(selection_req)
    elif selection == i18n("Edit vocabulary"):
        if (selection_req := edit.rmenu()) != 0:
            edit.set_menu(selection_req)


