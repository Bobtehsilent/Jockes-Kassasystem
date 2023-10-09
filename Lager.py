
#### b. Inventory (Class: Inventory)
   #- Create a class to manage the store's inventory.
   #- This class should have methods for adding products to inventory, 
   # updating quantities, and checking stock availability.

from datetime import datetime
import json
from Produkter import Produkt
from Kampanj import Kampanj
class Lager:
    def __init__(self):
        self.kampanjer = {}
        self.produkter = {}
    def lägg_till_produkt(self, produkt_id, produkt_pris, produkt_namn):
        if produkt_id in self.produkter:
            print(f"Produkt med id {produkt_id} existerar redan")
        else:
            ny_produkt = Produkt(produkt_id, produkt_namn, produkt_pris)
            self.produkter[produkt_id] = ny_produkt
    def uppdatera_produkt_pris(self, produkt_id, nytt_pris):
        if produkt_id in self.produkter:
            produkt = self.produkter[produkt_id]
            produkt.produkt_pris = nytt_pris
            print(f"Produkten med id {produkt_id} har uppdaterats med priset {nytt_pris}")
        else:
            print(f"Produkt med ID {produkt_id} existerar inte")
    def uppdatera_produkt_namn(self, produkt_id, nytt_namn):
        if produkt_id in self.produkter:
            produkt = self.produkter[produkt_id]
            produkt.produkt_namn = nytt_namn
            print(f"Produkten med id {produkt_id} har uppdaterats med namnet {nytt_namn}")
        else:
            print(f"Produkt med ID {produkt_id} existerar inte")
    def ta_bort_produkt(self, produkt_id):
        if produkt_id in self.produkter:
            del self.produkter[produkt_id]
        else:
            print(f"Produkten med id {produkt_id} existerar inte.")
    def sök_efter_produkt(self, namn):
        matchning = [produkt for produkt in self.produkter.values() if namn.lower() in produkt.produkt_namn.lower()]  # noqa: E501
        return matchning
    def hämta_produkt_info(self, produkt_id):
        if produkt_id in self.produkter:
            produkt = self.produkter[produkt_id]
            produkt_namn = produkt.produkt_namn
            per_pris = produkt.produkt_pris
            if produkt_namn in self.kampanjer:
                kampanj = self.kampanjer[produkt_namn]
                kampanj_pris = kampanj.kampanj_pris
                kampanj_start_datum = kampanj.kampanj_start_datum
                kampanj_slut_datum = kampanj.kampanj_slut_datum
                return produkt_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum
            else:
                return produkt_namn, per_pris, None, None
        else:
            return None, None
    def lägg_till_kampanj(self,produkt_namn, kampanj_namn, kampanj_pris):
        print(f"Försöker lägga till kampanj för produkten {produkt_namn}")
        if produkt_namn in self.produkter:
            kampanj_start_datum, kampanj_slut_datum = self.Skapa_kampanj_datum()
            print(f"Hämtat kampanj datum {kampanj_start_datum} - {kampanj_slut_datum}")
            if self.Kolla_om_datum(kampanj_start_datum) and self.Kolla_om_datum(kampanj_slut_datum):
                kampanj = Kampanj(kampanj_namn, produkt_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum)
                self.kampanjer[produkt_namn] = kampanj
                print(f"Kampanj för {produkt_namn} har lagts till.")
            else:
                print("Ogiltigt datumformat. Kampanjen har inte lagts till.")
        else:
            print(f"Produkten med namnet {produkt_namn} existerar inte.")
    def Skapa_kampanj_datum(self):
        while True:
            kampanj_start_datum = input("Skriv in startdatum för kampanjen (YYYY-MM-DD): ")
            kampanj_slut_datum = input("Skriv in slutdatum för kampanjen (YYYY-MM-DD): ")
            if self.Kolla_om_datum(kampanj_start_datum) == True and self.Kolla_om_datum(kampanj_slut_datum) == True:
                return kampanj_start_datum, kampanj_slut_datum
            else:
                print("Skriv i datumformatet YYYY-MM-DD")
                continue
    def Kolla_om_datum(self, datumstr):
        format = "%Y-%m-%d"
        try:
            datetime.strptime(datumstr, format)
            return True
        except ValueError:
            return False
    def uppdatera_kampanj(self, kampanj_namn, nytt_pris):
        if kampanj_namn in self.kampanjer:
            kampanj = self.kampanjer[kampanj_namn]
            kampanj.kampanj_pris = nytt_pris
            print(f"Kampanjen '{kampanj_namn}' har uppdateras med nytt pris: {nytt_pris}")
        else:
            print(f"Kampanj med namnet {kampanj_namn} existerar inte")
    def ta_bort_kampanj(self, kampanj_namn):
        if kampanj_namn in self.kampanjer:
            del self.kampanjer[kampanj_namn]
            print(f"Kampanjen '{kampanj_namn}' har tagits bort.")
        else:
            print(f"Kampanjen med namnet {kampanj_namn} existerar inte")
    def visa_lager(self):
        lager_str = "Produkter:\n"
        for produkt in self.produkter.values():
            lager_str += f"{produkt}" + "\n"
        lager_str += "Kampanjer\n"
        for kampanj in self.kampanjer.values():
            lager_str += f"{kampanj}" + "\n"
        return lager_str
    def sortera_produkter(self):
        sorterad = sorted(self.produkter.values(), key=lambda produkt: produkt.produkt_namn.lower())  # noqa: E501
        return sorterad
    def spara_filer(self, filnamn):
        with open(filnamn, "w") as fil:
            json.dump({'produkter': [produkt.formattera() for produkt in self.produkter.values()], 'kampanjer': [kampanj.formatera() for kampanj in self.kampanjer.values()]}, fil)  # noqa: E501
    def öppna_filer(self, filnamn):
        with open(filnamn, "r") as fil:
            data = json.load(fil)
            self.produkter = {}
            for produkt_data in data['produkter']:
                produkt = Produkt(produkt_data['produkt_id'], produkt_data['produkt_pris'], produkt_data['produkt_namn'])
                self.produkter[produkt.produkt_id] = produkt
            self.kampanjer = {}
            for kampanj_data in data['kampanjer']:
                kampanj = Kampanj(
                    kampanj_data['kampanj_namn'],
                    kampanj_data['kampanj_pris'],
                    kampanj_data['kampanj_start_datum'],
                    kampanj_data['kampanj_slut_datum'],
                )
                self.kampanjer[kampanj.produkt_namn] = kampanj
            