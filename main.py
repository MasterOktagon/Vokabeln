import color
import menu
import req
import edit

while (selection := menu.menu("Vokabelprogramm - CLI v2", ["Vokabeln abfragen", "Vokabelsätze bearbeiten", "", "Beenden"])) != "Beenden":
    match selection:
        case "Vokabeln abfragen":
            if (selection_req := req.rmenu()) != 0:
                req.req(selection_req)
        case "Vokabelsätze bearbeiten":
            if (selection_req := edit.rmenu()) != 0:
                edit.set_menu(selection_req)


