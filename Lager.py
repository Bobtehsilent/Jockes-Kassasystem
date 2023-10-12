
from datetime import datetime
import json
from Kvitton import Kvitto
from Produkter import Produkt
from Kampanj import Kampanj
class Lager:
    def __init__(self):
        self.kampanjer = {}
        self.produkter = {}
        self.kvitto = Kvitto()
    def lägg_till_produkt(self,produkt_id, produkt_namn,produkt_pris):
        produkt = Produkt(produkt_id, produkt_namn, produkt_pris)
        if produkt.produkt_id in self.produkter:
            print(f"Produkt med id {produkt.produkt_id} existerar redan")
        else:
            self.produkter[produkt.produkt_id] = produkt

    def uppdatera_produkt(self, produkt_id, attribut, nytt_värde):
        if attribut == 'name':
            produkt = self.produkter[produkt_id]
            produkt.produkt_namn = nytt_värde
            print(f"Produkten med id {produkt_id} har uppdaterats med namnet: {nytt_värde}")
        elif attribut == 'pris':
            produkt = self.produkter[produkt_id]
            produkt.produkt_pris = nytt_värde
            print(f"Produkten med id {produkt_id} har uppdaterats med priset: {nytt_värde}")

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
                current_date = datetime.now()
                if kampanj_start_datum <= current_date <= kampanj_slut_datum:
                    return produkt_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum
                return produkt_namn, per_pris
            else:
                return produkt_namn, per_pris, None, None
        else:
            raise Exception("Produkten finns inte")

    def lägg_till_kampanj(self,produkt_id, kampanj_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum):
        print(f"Försöker lägga till kampanj för produkten {produkt_id}")
        if produkt_id in self.produkter:
            print(f"Hämtat kampanj datum {kampanj_start_datum} - {kampanj_slut_datum}")
            if Kampanj.analysera_och_validera(kampanj_start_datum) and Kampanj.analysera_och_validera(kampanj_slut_datum):
                if kampanj_namn not in self.kampanjer:
                    kampanj = Kampanj(kampanj_namn, produkt_id, kampanj_pris, kampanj_start_datum, kampanj_slut_datum)
                    self.kampanjer[produkt_id] = kampanj
                    print(f"Kampanj {kampanj_namn} för {produkt_id} har lagts till.")
                else:
                    print(f"En kampanj med namnet {kampanj_namn} finns redan.")
            else:
                print("Ogiltigt datumformat. Kampanjen har inte lagts till.")
        else:
            print(f"Produkten med namnet {produkt_id} existerar inte.")
    def skapa_kampanj_datum(self):
        while True:
            kampanj_start_datum = input("Skriv in startdatum för kampanjen (YYYY-MM-DD): ")
            kampanj_slut_datum = input("Skriv in slutdatum för kampanjen (YYYY-MM-DD): ")

            analyserad_start_datum = Kampanj.analysera_och_validera(kampanj_start_datum)
            analyserad_slut_datum = Kampanj.analysera_och_validera(kampanj_slut_datum)

            if analyserad_start_datum and analyserad_slut_datum:
                if analyserad_start_datum >= analyserad_slut_datum:
                    print("Kampanjen måste ta slut efter startdatumet")
                else:
                    return kampanj_start_datum, kampanj_slut_datum
                
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
        try:
            lager_str = "Produkter:\n"
            for produkt_id, produkt in self.produkter.items():
                lager_str += f"{produkt}"
                if produkt_id in self.kampanjer:
                    kampanj = self.kampanjer[produkt_id]
                    lager_str += f" (Kampanj! Nytt pris: {kampanj.kampanj_pris} SEK)"
                lager_str += "\n"
        except Exception as e:
            lager_str += f"Error med produkt: {e}" + "\n"
        return lager_str
    
    def sortera_produkter(self):
        sorterad = sorted(self.produkter.values(), key=lambda produkt: produkt.produkt_namn.lower())  # noqa: E501
        return sorterad

    def spara_filer(self):
        try:
            data_att_spara = {
                'produkter': [produkt.till_dict() for produkt in self.produkter.values()], 
                'kampanjer': [kampanj.till_dict() for kampanj in self.kampanjer.values()],
            }
            with open("produkt_och_kampanj.json", "w") as f:
                json.dump(data_att_spara, f, indent=4)
            print("All data har sparats")
        except Exception as e:
            print(f"Error: Något gick fel vid sparande av data: {str(e)}")
                 
    def öppna_filer(self):
        try:
            with open("produkt_och_kampanj.json", "r") as fil:
                all_data = json.load(fil)
                self.produkter = {}
                for produkt_data in all_data['produkter']:
                    produkt = Produkt(produkt_data['produkt_id'], 
                                    produkt_data['produkt_namn'], 
                                    produkt_data['produkt_pris'])
                    self.produkter[produkt.produkt_id] = produkt
                self.kampanjer = {}
                for kampanj_data in all_data['kampanjer']:
                    kampanj = Kampanj(
                        kampanj_data['kampanj_namn'],
                        kampanj_data['produkt_id'],
                        kampanj_data['kampanj_pris'],
                        Kampanj.analysera_och_validera(kampanj_data['kampanj_start_datum']),
                        Kampanj.analysera_och_validera(kampanj_data['kampanj_slut_datum']),
                    )
                    self.kampanjer[kampanj.produkt_id] = kampanj
        except FileNotFoundError:
            print("Datafilen hittades inte. Startar med en tom fil")
        except json.JSONDecodeError:
            print("Datan är inte i ett giltigt JSON format. Börjar med en tom fil.")
        except Exception as e:
            print(f"Ett oväntat fel inträffade: {str(e)}")