from datetime import datetime
import json
import os
from Lager import Lager
from Kvitton import Kvitto

class ExitSubmenuException(Exception):
    pass
class Administrera:
    MENYER = {
        'main': [
            'Nytt kvitto',
            "Administration",
            "Avsluta"
],
        'admin': [
            'Sök kvitto',
            'Produktmeny',
            'Kampanjmeny',
            'Stäng ner Administration'
        ],
        'produkt': [
            'Lägg till produkt',
            'Ta bort produkt',
            'Visa lager',
            'Uppdatera existerande produkt',
            'Gå tillbaka'
        ],
        'kampanj': [
            'Lägg till kampanj',
            'Ta bort kampanj',
            'Uppdatera existerande kampanj',
            'Visa kampanj lager',
            'Gå tillbaka'
        ],
        'kvitto':[
            'Kvittot har dagens datum',
            'Välj ett datum att söka efter',
            'Gå tillbaka'
        ],
        'uppdatera': [
            'Uppdatera pris',
            'Uppdatera namn'
        ]
    }
    
    def __init__(self,lager,kvitto):
        self.lager = lager
        self.kvitto = kvitto
        self.FUNKTION_HANTERARE = {
            'main': {
            1: self.nytt_kvitto,
            2: self.admin_meny_val
        },
            'produkt': {
            1: self.lägg_till_vara,
            2: self.ta_bort_vara,
            3: self.visa_varulager,
            4: self.uppdatera_vara,
        },
            'kampanj': {
            1: self.ny_kampanj,
            2: self.ta_bort_kampanj,
            3: self.uppdatera_kampanj,
            4: self.visa_kampanj_lager,
        },
            'admin': {
            1: self.sök_kvitto_meny,
            2: self.produkt_meny,
            3: self.kampanj_meny
        },
            'kvitto': {
                
            }
    }

    def universal_input_hantering(self, prompt, input_type=int, 
                                  min_värde=None, max_värde=None, stäng_på_0=True):
        while True:
            val = input(prompt)
            if stäng_på_0 and (val == '0' or val == 0):
                raise ExitSubmenuException()
            try:
                if input_type == int:
                    val = int(val)
                    if min_värde is not None and max_värde is not None:
                        if val < min_värde or val > max_värde:
                            print(f"Mata in ett tal mellan {min_värde} "
                                  f"och {max_värde} tack")
                            continue
                elif input_type == float:
                    val == float(val)
                return val
            except ValueError:
                print("Error: Felaktig input format")

    def submeny_hanterare(self, menu_name):
        try:
            while True:
                val = self.print_meny(menu_name)
                if val == 0 and menu_name == 'main':
                    self.lager.spara_filer()
                    exit()
                elif val == 0:
                    break
                function_to_execute = self.FUNKTION_HANTERARE[menu_name].get(val)
                if function_to_execute:
                    function_to_execute()
        except ExitSubmenuException:
            return

    def gå_tillbaka_subval(self, värde):
        if värde == 0 or värde == '0':
            raise ExitSubmenuException()
    
    def print_meny(self, meny_namn):
        for idx, val in enumerate(self.MENYER[meny_namn]):
            if idx == len(self.MENYER[meny_namn]) -1:
                print(f"0. {val}")
            else:
                print(f"{idx + 1}. {val}")
        max_val = len(self.MENYER[meny_namn]) - 1
        if meny_namn == 'main':
            return self.universal_input_hantering(":", min_värde=0, max_värde=max_val, 
                                                  stäng_på_0=False)
        else:
            return self.universal_input_hantering(":", min_värde=0, max_värde=max_val)
    
    def sök_kvitto_meny(self):
        while True:
            val_för_sök_kvitto = self.print_meny('kvitto')
            if val_för_sök_kvitto == 1:
                sök_kriterie = datetime.now().strftime("%Y%m%d")
            elif val_för_sök_kvitto == 2:
                sök_kriterie = input("Ange datum (YYYY-MM-DD): ")
            elif val_för_sök_kvitto == 0:
                return
            matchande_kvitton = self.kvitto._sök_kvitto(sök_kriterie)
            if matchande_kvitton:
                for matchande_kvitto in matchande_kvitton:
                    print(matchande_kvitto)
            else:
                print("Fanns inga kvitton för angivna datumet.")
                
    def produkt_meny(self):
        self.submeny_hanterare('produkt')

    def lägg_till_vara(self):
        try:
            produkt_id = input("Välj id för produkten: ")
            produkt_namn = input("Välj ett namn för produkten: ")
            produkt_pris = float(input("Välj ett pris på varan: "))
            self.lager.lägg_till_produkt(produkt_id, produkt_namn, produkt_pris)
            print(f"Produkten {produkt_namn} har lagts till med id {produkt_id}")
        except ExitSubmenuException:
            return
        except ValueError:
            print("Error: Välj ett positivt pris tack")

    def ta_bort_vara(self):
        produkt_id = input("Vad är ID på produkten du vill ta bort?: ")
        self.lager.ta_bort_produkt(produkt_id)

    def visa_varulager(self):
        print(self.lager.visa_produkt_lager())

    def uppdatera_vara(self):
        try:
            val_uppdatera = self.print_meny('uppdatera')
            if val_uppdatera == 1:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                nytt_namn = input("Ange nytt namn för varan: ")
                self.lager.uppdatera_produkt(produkt_id,'name', nytt_namn)
            elif val_uppdatera == 2:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                nytt_pris = int(input("Ange nytt pris för varan: "))
                self.lager.uppdatera_produkt(produkt_id,'pris', nytt_pris)
        except ValueError:
            print("Error: Ange ett positivt heltal.")
    
    def kampanj_meny(self):
        self.submeny_hanterare('kampanj')

    def ny_kampanj(self):
        produkt = input("Skriv produktid för produkten du "
                                "ha på kampanj\n: ")
        if produkt == '0':
            return
        produkt = self.lager.sök_efter_produkt(produkt)
        if not produkt:
            print("Produkten finns inte, försök igen")
            return
        kampanj_namn = input("Vad ska kampanjen heta: ")
        try:
            kampanj_pris = float(input("Mata in nya kampanj priset: "))
            kampanj_start_datum, kampanj_slut_datum = \
                self.lager.skapa_kampanj_datum()
        except ValueError:
            print("Felaktig pris. Vänligen mata in ett numeriskt värde")
        self.lager.lägg_till_kampanj(produkt.produkt_id, kampanj_namn, kampanj_pris,\
                                     kampanj_start_datum, kampanj_slut_datum)
        
    def ta_bort_kampanj(self):
        self.lager.visa_kampanj_lager()
        produkt_id = input("Ange produktid för produkten vars " 
                        "kampanj du vill ta bort: ")
        kampanj_namn = input("Ange namn på kampanjen du vill ta bort: ").lower()
        if kampanj_namn == '0' or produkt_id == '0':
            return
        self.lager.ta_bort_kampanj(produkt_id, kampanj_namn)

    def uppdatera_kampanj(self):
        produkt_id = input("Ange produktid för att "
                             "se vilka kampanjer produkten har: ")
        kampanjer = self.lager.visa_kampanjer_för_produkt(produkt_id)
        if not kampanjer:
            print("Ingen kampanj att uppdatera")
            return
        try:
            val_kampanj = int(input("Ange numret på kampanjen"
                                        " du vill uppdatera: "))
            assert 1 <= val_kampanj <= len(kampanjer)

            kampanj_namn = kampanjer[val_kampanj-1]
            nytt_pris = float(input("Ange det nya kampanjpriset: "))
            assert nytt_pris > 0
            self.lager.uppdatera_kampanj(produkt_id, kampanj_namn, nytt_pris)
        except ValueError:
            print("Error: Ange ett positivt tal.")
        except AssertionError:
            print(f"Error: Ange ett nummer mellan 1 och {len(kampanjer)}.")
    def visa_kampanj_lager(self):
        print(self.lager.visa_kampanj_lager())

    def dela_kommandon(self):
        while True:
            kassa_input = input(": ")
            delar = kassa_input.split(' ')
            if len(delar) == 2:
                return delar[0], delar[1]
            elif len(delar) == 1:
                if delar[0].lower() == "pay" or delar[0].lower() == 'q':
                    return delar
            print("För få tecken inskrivna, försök igen")

    def nytt_kvitto(self):
        print("Kassa 1")
        self.kvitto.kvitto_nummer += 1
        while True:
            print("Kommandon: <produktid> <Space> <antal> | PAY")
            delar = self.dela_kommandon()
            if not delar:
                print("Ogiltigt kommando. Försök igen")
                continue
            elif delar[0] == '0':
                break
            elif delar[0].lower() == 'pay':
                self.kvitto.generera_kvitto()
                self.kvitto.skriv_kvitto()
                self.kvitto.resetta_kvitto()
                break
            else:
                produkt_id = delar[0]
                antal = delar[1]
                try:
                    namn, belopp, kampanj_start_datum, kampanj_slut_datum = \
                        self.lager.hämta_produkt_info(produkt_id)
                except IndexError:
                    print("Error: produkt informationen är ej komplett")
                except Exception as e:
                    print(f"Error: {e}")
                    continue
                try:
                    self.kvitto.lägg_till(namn, int(antal), float(belopp), 
                                          kampanj_start_datum, kampanj_slut_datum)
                except ValueError:
                    print("Mata in enligt formatet <Produktid> <Antal> eller PAY")

    def admin_meny_val(self):
        self.submeny_hanterare('admin')
    
    def main(self):
        self.submeny_hanterare('main')

@staticmethod
def uppstart():
    kvitto = Kvitto()
    lager = Lager()
    if not os.path.isfile("produkt_och_kampanj.json"):
        default_data = {'produkter': [], 'kampanjer': []}
        with open("produkt_och_kampanj.json", "a") as f:    
            json.dump(default_data, f)
    lager.öppna_filer()
    kvitto.öppna_kvitto_nummer()
    admin_meny = Administrera(lager, kvitto)
    admin_meny.main()

if __name__ == "__main__":
    uppstart()
