import helper_kartenspiel_functional as help
import random
from functools import reduce

N=13 # Anzahle der Karten im Spiel

## Zustand "state" des Programms
state = {"zufallsgenerator": random.Random(0), \
         "spieler1_kartenspiel" : help.kartenspiel(N),\
         "spieler2_kartenspiel" : help.kartenspiel(N),\
         "spieler1_karte" : None,
         "spieler2_karte" : None,
         "preiskarten" : help.kartenspiel(N),\
         "aktuelle_preiskarte" : None,\
         "spieler1_strategie" : help.spiele_zufällige_karte,\
         "spieler2_strategie" : help.spiele_den_wert_der_preiskarte,\
         "spieler1_punkte" : 0,\
         "spieler2_punkte" : 0}

#  Das eigentliche Spiel
abbruchkriterium = lambda states: not states[-1]["preiskarten"]
states = help.spiel_rekursiv((state,), abbruchkriterium=abbruchkriterium,spielrunde=help.spielrunde)

#### Dokumentation
# Nebeneffekt: Drucke die gesamte Spieldokumentation
print(reduce(lambda x,y: x+"\n"+y, map(help.rundendokumentation, states[1:]))\
      +"\n"\
        +help.auswertung_am_ende(states[-1]["spieler1_punkte"],states[-1]["spieler2_punkte"]))
