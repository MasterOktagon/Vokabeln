import color
import menu
import req

while (selection := menu.menu("Vokabelprogramm - CLI v2", ["Vokabeln abfragen", "Vokabelsätze bearbeiten", "", "Beenden"])) != "Beenden":
    match selection:
        case "Vokabeln abfragen":
            if (selection_req := req.rmenu()) != 0:
                req.req(selection_req)
        case "Vokabelsätze bearbeiten":
            pass


