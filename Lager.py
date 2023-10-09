
#### b. Inventory (Class: Inventory)
   #- Create a class to manage the store's inventory.
   #- This class should have methods for adding products to inventory, 
   # updating quantities, and checking stock availability.

import json
from Produkter import Produkt
from Kampanj import Kampanj
class Lager:
    def __init__(self):
        self.kampanjer = {}
        self.produkter = {}
    def lägg_till_produkt(self, produktId, produktPris, produktNamn):
        if produktId in self.produkter:
            print(f"Produkt med id {produktId} existerar redan")
        else:
            ny_produkt = Produkt(produktId, produktNamn, produktPris)
            self.produkter[produktId] = ny_produkt
    def uppdatera_produkt(self, produktId, nyttPris):
        if produktId in self.produkter:
            produkt = self.produkter[produktId]
            produkt.produktPris = nyttPris
        else:
            print(f"Produkt med ID {produktId} existerar inte")
    def ta_bort_produkt(self, produktId):
        if produktId in self.produkter:
            del self.produkter[produktId]
        else:
            print(f"Produkten med id {produktId} existerar inte.")
    def lägg_till_kampanj(self, kampanj):
        if kampanj.kampanjNamn in self.kampanjer:
            print("Kampanj med namnet {kampanj.kampanjNamn} existerar inte")
        else:
            self.kampanjer[kampanj.kampanjNamn] = kampanj
    def uppdatera_kampanj(self, kampanjNamn, nyttPris):
        if kampanjNamn in self.kampanjer:
            kampanj = self.kampanjer[kampanjNamn]
            kampanj.kampanjPris = nyttPris
        else:
            print(f"Kampanj med namnet {kampanjNamn} existerar inte")
    def ta_bort_kampanj(self, kampanjNamn):
        if kampanjNamn in self.kampanjer:
            del self.kampanjer[kampanjNamn]
        else:
            print(f"Kampanjen med namnet {kampanjNamn} existerar inte")
    def sök_efter_produkt(self, namn):
        matchning = [produkt for produkt in self.produkter.values() if namn.lower() in produkt.produktNamn.lower()]  # noqa: E501
        return matchning
    def visa_lager(self):
        lager_str = "Produkter:\n"
        for produkt in self.produkter.values():
            lager_str += f"{produkt}" + "\n"
        lager_str += "Kampanjer\n"
        for kampanj in self.kampanjer.values():
            lager_str += f"{kampanj}" + "\n"
        return lager_str
    def sortera_produkter(self):
        sorterad = sorted(self.produkter.values(), key=lambda produkt: produkt.produktNamn.lower())  # noqa: E501
        return sorterad
    def spara_filer(self, filnamn):
        with open(filnamn, "w") as fil:
            json.dump({'produkter': self.produkter, 'kampanjer': self.kampanjer}, fil)
    def öppna_filer(self, filnamn):
        with open(filnamn, "r") as fil:
            data = json.load(fil)
            self.produkter = data['produkter']
            self.kampanjer = data['kampanjer']