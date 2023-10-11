
#### b. Inventory (Class: Inventory)
   #- Create a class to manage the store's inventory.
   #- This class should have methods for adding products to inventory, 
   # updating quantities, and checking stock availability.

from datetime import datetime
import json
from Kvitton import Kvitto
from Produkter import Produkt
from Kampanj import Kampanj
class Lager:
    def __init__(self):
        self.kampanjer = {}
        self.produkter = {}
    def spara_produkt_i_dict(self, produkt_id, tillägg):
        self.produkter[produkt_id] = tillägg

    def lägg_till_produkt(self,produkt):
        if produkt.produkt_id in self.produkter:
            print(f"Produkt med id {produkt.produkt_id} existerar redan")
        else:
            self.produkter[produkt.produkt_id] = produkt
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
    def sök_efter_produkt(self, identifier):
        if identifier in self.produkter:
            return self.produkter[identifier]
        else:
            matchning = [produkt for produkt in self.produkter.values() if identifier.lower() in produkt.produkt_namn.lower()]  # noqa: E501
            if matchning:
                return matchning
            else:
                return None
    def hämta_produkt_info(self, produkt_id):
        if produkt_id in self.produkter:
            produkt = self.produkter[produkt_id]
            produkt_namn = produkt.produkt_namn
            per_pris = produkt.produkt_pris
            if produkt_id in self.kampanjer:
                kampanj = self.kampanjer[produkt_id]
                kampanj_pris = kampanj.kampanj_pris
                kampanj_start_datum = kampanj.kampanj_start_datum
                kampanj_slut_datum = kampanj.kampanj_slut_datum
                return produkt_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum
            else:
                return produkt_namn, per_pris, None, None
        else:
            return None, None

    def lägg_till_kampanj(self,produkt_id, kampanj_namn, kampanj_pris):
        print(f"Försöker lägga till kampanj för produkten {produkt_id}")
        if produkt_id in self.produkter:
            kampanj_start_datum, kampanj_slut_datum = self.Skapa_kampanj_datum()
            print(f"Hämtat kampanj datum {kampanj_start_datum} - {kampanj_slut_datum}")
            if self.Kolla_om_datum(kampanj_start_datum) and self.Kolla_om_datum(kampanj_slut_datum):
                kampanj = Kampanj(kampanj_namn, produkt_id, kampanj_pris, kampanj_start_datum, kampanj_slut_datum)
                self.kampanjer[produkt_id] = kampanj
                print(f"Kampanj för {produkt_id} har lagts till.")
            else:
                print("Ogiltigt datumformat. Kampanjen har inte lagts till.")
        else:
            print(f"Produkten med namnet {produkt_id} existerar inte.")
    def Skapa_kampanj_datum(self):
        while True:
            kampanj_start_datum = input("Skriv in startdatum för kampanjen (YYYY-MM-DD): ")
            kampanj_slut_datum = input("Skriv in slutdatum för kampanjen (YYYY-MM-DD): ")
            if kampanj_start_datum >= kampanj_slut_datum:
                raise ValueError("Kampanjen måste ta slut efter startdatumet")
            if self.Kolla_om_datum(kampanj_start_datum) is True and self.Kolla_om_datum(kampanj_slut_datum) is True:
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
    def uppdatera_kvitto_nummer(self, kvitto, nummer):
        kvitto.set_kvitto_nummer(nummer)
    def hämta_kvitto_nummer(self, kvitto):
        kvitto.Get_kvitto_nummer(kvitto)
    def spara_filer(self, filnamn, kvitto_nummer):
        with open(filnamn, "w") as fil:
            json.dump(
                {
                    'produkter': [produkt.formattera() for produkt in self.produkter.values()], 
                    'kampanjer': [kampanj.formattera() for kampanj in self.kampanjer.values()],
                    'kvitto_nummer': kvitto_nummer
                    }, fil
                ) 
    def öppna_filer(self, filnamn, kvitto_instans):
        with open(filnamn, "r") as fil:
            data = json.load(fil)
            self.produkter = {}
            for produkt_data in data['produkter']:
                produkt = Produkt(produkt_data['produkt_id'], produkt_data['produkt_namn'], produkt_data['produkt_pris'])
                self.produkter[produkt.produkt_id] = produkt
                self.produkter[produkt.produkt_namn] = produkt
            self.kampanjer = {}
            for kampanj_data in data['kampanjer']:
                kampanj = Kampanj(
                    kampanj_data['kampanj_namn'],
                    kampanj_data['produkt_namn'],
                    kampanj_data['kampanj_pris'],
                    kampanj_data['kampanj_start_datum'],
                    kampanj_data['kampanj_slut_datum'],
                )
                self.kampanjer[kampanj.produkt_namn] = kampanj
            kvitto_nummer = data.get('kvitto_nummer', 0)
            kvitto_instans.set_kvitto_nummer(kvitto_nummer)