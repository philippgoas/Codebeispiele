import random

def auswertung_am_ende(spieler1_punkte,spieler2_punkte):
    doku = "Finaler Spielstand: {p_sp1} zu {p_sp2}".format(p_sp1 = spieler1_punkte, p_sp2 = spieler2_punkte)
    if spieler1_punkte>spieler2_punkte:
        doku += "\n Spieler 1 hat gewonnen!"
    elif spieler1_punkte<spieler2_punkte:
        doku += "\n Spieler 2 hat gewonnen!"
    else:
        doku += "\n Unentschieden!"
    return doku

def kartenspiel(N):
    return tuple(range(1,N+1))

def mischen(kartenspiel, zufallsgenerator):
    neues_kartenspiel = list(kartenspiel)
    # Kopie des Zufallsgenerators erzeugen um diesen unverändert zu lassen
    neuer_zufallsgenerator = random.Random()
    neuer_zufallsgenerator.setstate(zufallsgenerator.getstate())

    neuer_zufallsgenerator.shuffle(neues_kartenspiel)
    return tuple(neues_kartenspiel), neuer_zufallsgenerator

def auswerten_der_spielrunde(spieler1_karte,spieler2_karte,spieler1_punkte,spieler2_punkte,aktuelle_preiskarte):
    # Vergleich der Wertigkeit der Karten
    # Falls spieler1_karte>spieler2_karte: 
    # ## erhöhe spieler1_punkte um preiskarte
    if spieler1_karte>spieler2_karte:
        spieler1_punkte += aktuelle_preiskarte
    # sonst falls spieler2_karte>spieler1_karte:
    # ## erhöhe spieler2_punkte um preiskarte
    elif spieler2_karte>spieler1_karte:
        spieler2_punkte += aktuelle_preiskarte

    return spieler1_punkte, spieler2_punkte

## Strategien der Spieler
def spiele_zufällige_karte(kartenspiel, preiskarte, zufallsgenerator):
    return ziehe_zufällige_karte(kartenspiel, zufallsgenerator)

def ziehe_zufällige_karte(kartenspiel, zufallsgenerator):
    neuer_zufallsgenerator = random.Random()
    neuer_zufallsgenerator.setstate(zufallsgenerator.getstate())
    karte = neuer_zufallsgenerator.choice(kartenspiel)
    return karte, kartenspiel_ohne_karte(kartenspiel, karte), neuer_zufallsgenerator

def spiele_den_wert_der_preiskarte(kartenspiel, preiskarte, zufallsgenerator):
    return preiskarte, kartenspiel_ohne_karte(kartenspiel, preiskarte), zufallsgenerator

def kartenspiel_ohne_karte(kartenspiel, karte):
    neues_kartenspiel = list(kartenspiel)
    neues_kartenspiel.remove(karte)
    return tuple(neues_kartenspiel)

def rundendokumentation(state):

    doku = "Gezogen wurde die Preiskarte "+ str(state["aktuelle_preiskarte"]) + "\n"
    doku += "Spieler 1 spielt eine {}, Spieler 2 spielt eine {}".format(state["spieler1_karte"], state["spieler2_karte"])
    if state["spieler1_karte"]>state["spieler2_karte"]:
        doku += "\n Spieler 1 gewinnt die Runde!"
    elif state["spieler1_karte"]<state["spieler2_karte"]: 
        doku += "\n Spieler 2 gewinnt die Runde!"
    else:
        doku += "\n Unentschieden - niemand bekommt Punkte."
    
    doku += "\n Es steht {p_sp1} zu {p_sp2}".format(p_sp1 = state["spieler1_punkte"], p_sp2 = state["spieler2_punkte"])

    return doku

def spielrunde(state):
    # Ziehe die oberste Preiskarte -> Variable preiskarte (eine Zahl)
    aktuelle_preiskarte, preiskarten, zufallsgenerator = ziehe_zufällige_karte(state["preiskarten"], state["zufallsgenerator"])
    
    # Auswahl der Karten von Spieler 1 und Spieler 2 
    spieler1_karte, spieler1_kartenspiel, zufallsgenerator  = state["spieler1_strategie"](state["spieler1_kartenspiel"], aktuelle_preiskarte, zufallsgenerator)
    spieler2_karte, spieler2_kartenspiel, zufallsgenerator = state["spieler2_strategie"](state["spieler2_kartenspiel"], aktuelle_preiskarte, zufallsgenerator)

    # Auswerten der Runde -> Update der Punkte
    spieler1_punkte, spieler2_punkte = auswerten_der_spielrunde(spieler1_karte,\
                                                                spieler2_karte,\
                                                                state["spieler1_punkte"],\
                                                                state["spieler2_punkte"],\
                                                                aktuelle_preiskarte)
    return {"zufallsgenerator": zufallsgenerator, \
         "spieler1_kartenspiel" : spieler1_kartenspiel,\
         "spieler2_kartenspiel" : spieler2_kartenspiel,\
         "spieler1_karte" : spieler1_karte,\
         "spieler2_karte" : spieler2_karte,\
         "preiskarten" : preiskarten,\
         "aktuelle_preiskarte" : aktuelle_preiskarte,\
         "spieler1_strategie" : state["spieler1_strategie"],\
         "spieler2_strategie" : state["spieler2_strategie"],\
         "spieler1_punkte" : spieler1_punkte,\
         "spieler2_punkte" : spieler2_punkte}

def spiel_rekursiv(states, abbruchkriterium, spielrunde):
    if abbruchkriterium(states):
        return states
    else:
        return spiel_rekursiv(states + (spielrunde(states[-1]), ), abbruchkriterium, spielrunde)


