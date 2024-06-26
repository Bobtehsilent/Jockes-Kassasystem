from datetime import datetime
import json
from Produkter import Produkt
from Kampanj import Kampanj

class Lager: #Funktionalitets klassen har jag tänkt det som. Den tar all information från produkt/kampanj och sätter ihop pusslet
    def __init__(self):
        self.kampanjer = {}
        self.produkter = {}
#Generellt är alla funktioner självförklarande i namnet
    def lägg_till_produkt(self,produkt_id, produkt_namn, produkt_pris, pris_typ):
        pris_typ_mapping = {1: 'kilo', 2: 'styck'}
        produkt = Produkt(produkt_id, produkt_namn, produkt_pris, pris_typ_mapping[pris_typ])
        if produkt.produkt_id in self.produkter:
            print(f"Produkt med id {produkt.produkt_id} existerar redan")
        else:
            self.produkter[produkt.produkt_id] = produkt
            print(f"Produkten {produkt_namn} har lagts till med id {produkt_id}")

    def uppdatera_produkt(self, produkt_id, attribut, nytt_värde):
        if attribut == 'name':
            produkt = self.produkter[produkt_id]
            produkt.produkt_namn = nytt_värde
            print(f"Produkten med id {produkt_id} "
                  f"har uppdaterats med namnet: {nytt_värde}")
        elif attribut == 'pris':
            produkt = self.produkter[produkt_id]
            produkt.produkt_pris = nytt_värde
            print(f"Produkten med id {produkt_id}"
                  f" har uppdaterats med priset: {nytt_värde}")

    def ta_bort_produkt(self, produkt_id):
        if produkt_id in self.produkter:
            del self.produkter[produkt_id]
        if produkt_id in self.kampanjer:
            del self.kampanjer[produkt_id]
        else:
            print(f"Produkten med id {produkt_id} existerar inte.")

    def sök_efter_produkt(self, identifier):
        if identifier in self.produkter:
            return self.produkter[identifier]
        else:
            matchning = [produkt for produkt in self.produkter.values() 
                         if identifier.lower() in produkt.produkt_namn.lower()] 
            if matchning:
                return matchning
            else:
                return None
            
    def hämta_produkt_info(self, produkt_id): #Viktig funktion, vid handling hämtar denna funktion all info från dictionaryn.
        if produkt_id in self.produkter:
            produkt = self.produkter[produkt_id]
            produkt_namn = produkt.produkt_namn
            per_pris = produkt.produkt_pris
            pris_typ = produkt.pris_typ
            if produkt_id in self.kampanjer:
                best_kampanj = None
                current_date = datetime.now()
                for _, kampanj in self.kampanjer[produkt_id].items():
                    kampanj_start_datum = kampanj.kampanj_start_datum
                    kampanj_slut_datum = kampanj.kampanj_slut_datum
                    if kampanj_start_datum <= current_date <= kampanj_slut_datum:
                        if best_kampanj is None or \
                            kampanj.kampanj_pris < best_kampanj.kampanj_pris:
                            best_kampanj = kampanj
                if best_kampanj is not None and best_kampanj.kampanj_pris < per_pris:
                    return produkt_namn, best_kampanj.kampanj_pris, pris_typ , \
                        best_kampanj.kampanj_start_datum, best_kampanj.kampanj_slut_datum
            return produkt_namn, per_pris, pris_typ, None, None
        else:
            raise ValueError(f"Produkt med id {produkt_id} finns inte")
        

    def lägg_till_kampanj(self,produkt_id, kampanj_namn, kampanj_pris, 
                          kampanj_start_datum, kampanj_slut_datum):
        if produkt_id in self.produkter:
            if isinstance(kampanj_start_datum, datetime) and isinstance(kampanj_slut_datum, datetime):
                if produkt_id not in self.kampanjer:
                    self.kampanjer[produkt_id] = {}
                if kampanj_namn not in self.kampanjer[produkt_id]:
                    kampanj = Kampanj(kampanj_namn, produkt_id, kampanj_pris,\
                                       kampanj_start_datum, kampanj_slut_datum)
                    self.kampanjer[produkt_id][kampanj_namn] = kampanj
                    print(f"Kampanj {kampanj_namn} för {produkt_id} har lagts till.")
                else:
                    print(f"En kampanj med namnet {kampanj_namn} finns redan.")
            else:
                print("Ogiltigt datumformat. Kampanjen har inte lagts till.")
        else:
            print(f"Produkten med namnet {produkt_id} existerar inte.")
                
    def visa_kampanjer_för_produkt(self, produkt_id):
        kampanj_lista = []
        if produkt_id in self.kampanjer:
            for id, kampanj_namn in enumerate(self.kampanjer[produkt_id].keys(), 1):
                print(f"{id}. {kampanj_namn}")
                kampanj_lista.append(kampanj_namn)
        else:
            print(f"Inga kampanjer hittades för produkt {produkt_id}.")
        return kampanj_lista
    
    def uppdatera_kampanj(self, produkt_id, kampanj_namn,  
                          nytt_namn=None, nytt_pris=None,
                          nytt_start_datum=None, nytt_slut_datum=None):
        kampanj = self.kampanjer[produkt_id][kampanj_namn]
        if nytt_namn is not None and nytt_namn != kampanj_namn:
            self.kampanjer[produkt_id][nytt_namn] = \
                (self.kampanjer[produkt_id].pop(kampanj_namn))
            print(f"Kampanjen '{kampanj_namn}' för produkten {produkt_id}" 
              f" har uppdaterats med nytt namn: {nytt_namn}.")
        if nytt_pris is not None:
            kampanj.kampanj_pris = nytt_pris
            print(f"Kampanjen '{kampanj_namn}' för produkten {produkt_id}" 
              f" har uppdaterats med nytt pris: {nytt_pris} kr.")
        if nytt_start_datum is not None and nytt_slut_datum is not None:
            kampanj.kampanj_start_datum = nytt_start_datum
            kampanj.kampanj_slut_datum = nytt_slut_datum
            print(f"Kampanjen '{kampanj_namn}' för produkten {produkt_id}" 
              f" har uppdaterats med nya datum: {nytt_start_datum:%Y-%m-%d} - {nytt_slut_datum:%Y-%m-%d}.")

    def ta_bort_kampanj(self, produkt_id, kampanj_namn):
        try:
            if produkt_id in self.kampanjer and\
                  kampanj_namn in self.kampanjer[produkt_id]:
                del self.kampanjer[produkt_id][kampanj_namn]
                print(f"Kampanjen '{kampanj_namn}' för "
                      f"produkten {produkt_id} har tagits bort")
                if not self.kampanjer[produkt_id]:
                    del self.kampanjer[produkt_id]
            else:
                print(f"Kampanjen med namnet {kampanj_namn} "
                      f"för produkten {produkt_id} existerar inte.")
        except Exception as e:
            print(f"Det uppstod ett fel vid borttagning av kampanj: {str(e)}")
          
    def visa_produkt_lager(self):
        lager_str = "Produkter:\n"
        try:
            for produkt_id, produkt in self.produkter.items():
                lager_str += f"{produkt}"
                if produkt_id in self.kampanjer:
                    antal_kampanjer = len(self.kampanjer[produkt_id])
                    lager_str += f" ({antal_kampanjer} " \
                        f"kampanj{'er' if antal_kampanjer >1 else''} "\
                            f"tillgänglig{'a'  if antal_kampanjer > 1 else ''})"
                lager_str += "\n"
        except Exception as e:
            lager_str += f"Error med produkt: {e}" + "\n"
        return lager_str
    
    def visa_kampanj_lager(self):
        lager_str = "Kampanjer:\n"
        try:
            for produkt_id, kampanjer in self.kampanjer.items():
                produkt_namn = self.produkter[produkt_id].produkt_namn
                lager_str += f"{produkt_namn} ({produkt_id}):\n"
                for kampanj_namn, kampanj in kampanjer.items():
                    lager_str += f"  Kampanj: {kampanj_namn}\n"
                    lager_str += f"    Nytt pris: {kampanj.kampanj_pris} SEK\n"
                    start_datum = kampanj.kampanj_start_datum.strftime('%Y-%m-%d')
                    slut_datum = kampanj.kampanj_slut_datum.strftime('%Y-%m-%d')
                    lager_str += f"    Start datum: {start_datum}\n"
                    lager_str += f"    Slut datum: {slut_datum}\n"
                lager_str += "\n"
        except Exception as e:
            lager_str += f"Error med kampanj: {e}\n" 
        return lager_str  

    def ladda_meny_och_funktion_hanterare(self, admin): #Ser väldigt konstig ut men den laddar alla menyer och menyval från en jsonfil.
        with open('menyer_och_funktioner.json') as f:
            data = json.load(f)
        admin.MENYER = data['MENYER']
        funktion_namn_till_metod = {
            "nytt_kvitto":admin.nytt_kvitto,
            "admin_meny_val":admin.admin_meny_val,
            "lägg_till_vara":admin.lägg_till_vara,
            "ta_bort_vara":admin.ta_bort_vara,
            "visa_varulager":admin.visa_varulager,
            "uppdatera_vara":admin.uppdatera_vara,
            "ny_kampanj":admin.ny_kampanj,
            "ta_bort_kampanj":admin.ta_bort_kampanj,
            "uppdatera_kampanj":admin.uppdatera_kampanj,
            "visa_kampanj_lager":admin.visa_kampanj_lager,
            "sök_kvitto_meny":admin.sök_kvitto_meny,
            "produkt_meny":admin.produkt_meny,
            "kampanj_meny":admin.kampanj_meny,
            "uppdatera_produkt_namn":admin.uppdatera_produkt_namn,
            "uppdatera_produkt_pris":admin.uppdatera_produkt_pris,
            "uppdatera_kampanj_namn":admin.uppdatera_kampanj_namn,
            "uppdatera_kampanj_pris":admin.uppdatera_kampanj_pris,
            "uppdatera_kampanj_datum":admin.uppdatera_kampanj_datum,
            "sök_dagens_kvitto":admin.sök_dagens_kvitto,
            "sök_datum_kvitto":admin.sök_datum_kvitto
        }
        admin.FUNKTION_HANTERARE = {}
        for meny_namn, funktion_namn in data['FUNKTION_HANTERARE'].items():
            admin.FUNKTION_HANTERARE[meny_namn] = {
                int(key): funktion_namn_till_metod[value]
                for key, value in funktion_namn.items()}

    def spara_produkt_och_kampanj(self): #Sparar ner produkter/kampanjer om nya blivit tillagda i sin json fil.
        try:
            produkter_data = [produkt.till_dict() \
                              for produkt in self.produkter.values()]
            kampanjer_data = {}
            for produkt_id, kampanjer in self.kampanjer.items():
                kampanjer_data[produkt_id] = {namn: kampanj.till_dict() \
                                              for namn, kampanj in kampanjer.items()}
            data_att_spara = {
                'produkter': produkter_data, 
                'kampanjer': kampanjer_data,
            }
            with open("produkt_och_kampanj.json", "w") as f:
                json.dump(data_att_spara, f, indent=4)
            print("All data har sparats")
        except Exception as e:
            print(f"Error: Något gick fel vid sparande av data: {str(e)}")
                 
    def ladda_produkt_och_kampanj(self): #Laddar all data från json filer
        try:
            with open("produkt_och_kampanj.json", "r") as fil:
                all_data = json.load(fil)
                self.produkter = {}
                for produkt_data in all_data['produkter']:
                    produkt = Produkt(produkt_data['produkt_id'], 
                                    produkt_data['produkt_namn'], 
                                    produkt_data['produkt_pris'],
                                    produkt_data['pris_typ'])
                    self.produkter[produkt.produkt_id] = produkt
                self.kampanjer = {}
                for produkt_id, kampanjer_av_produkt in all_data['kampanjer'].items():
                    self.kampanjer[produkt_id] = {}
                    for kampanj_namn, kampanj_data in kampanjer_av_produkt.items():
                        kampanj = Kampanj(
                            kampanj_data['kampanj_namn'],
                            kampanj_data['produkt_id'],
                            kampanj_data['kampanj_pris'],
                            Kampanj.analysera_och_validera(kampanj_data['kampanj_start_datum']),
                            Kampanj.analysera_och_validera(kampanj_data['kampanj_slut_datum']),)
                        self.kampanjer[produkt_id][kampanj_namn] = kampanj
        except FileNotFoundError:
            print("Datafilen hittades inte. Startar med en tom fil")
        except json.JSONDecodeError:
            print("Datan är inte i ett giltigt JSON format. Börjar med en tom fil.")
        except Exception:
            pass