from datetime import datetime
import json
import os
from Lager import Lager
from Kvitton import Kvitto

class ExitSubmenuException(Exception):
    def __init__(self, tillbaka_till_meny=None):
        self.tillbaka_till_meny = tillbaka_till_meny 

class Administrera:
    def __init__(self,lager,kvitto):
        self.lager = lager
        self.kvitto = kvitto
        self.MENYER = {}
        self.FUNKTION_HANTERARE = {}

    def universal_input_hantering(self, prompt, input_type=str, 
                                  min_värde=None, max_värde=None, stäng_på_0=True):
        while True:
            val = input(prompt)
            if stäng_på_0 and (val == '0' or val == 0):
                print("Går tillbaka.")
                raise ExitSubmenuException()
            try:
                if input_type == int:
                    val = int(val)
                    if min_värde is not None and max_värde is not None:
                        if val < min_värde or val > max_värde:
                            print("Vänligen in ett tal mellan" 
                                f" {min_värde} och {max_värde}")
                            continue
                elif input_type == float:
                    val == float(val)
                return val
            except ValueError:
                print("Error: Felaktig input format")

    def submeny_hanterare(self, menu_name, *args):
        try:
            while True:
                val = self.print_meny(menu_name)
                if val == 0 and menu_name == 'main':
                    self.lager.spara_produkt_och_kampanj()
                    exit()
                elif val == 0:
                    break
                function_to_execute = self.FUNKTION_HANTERARE[menu_name].get(val)
                if function_to_execute:
                    function_to_execute(*args)
        except ExitSubmenuException as e:
            if e.tillbaka_till_meny is not None:
                self.submeny_hanterare(e.tillbaka_till_meny, *args)
    
    def print_meny(self, meny_namn):
        for idx, val in enumerate(self.MENYER[meny_namn]):
            if idx == len(self.MENYER[meny_namn]) -1:
                print(f"0. {val}")
            else:
                print(f"{idx + 1}. {val}")
        max_val = len(self.MENYER[meny_namn]) - 1
        if meny_namn == 'main':
            return self.universal_input_hantering(":", min_värde=0, max_värde=max_val, 
                                                  input_type=int,stäng_på_0=False)
        else:
            return self.universal_input_hantering(":", min_värde=0, max_värde=max_val, 
                                                  input_type=int)
        
    def sök_kvitto_meny(self):
        self.submeny_hanterare('kvitto')

    def sök_dagens_kvitto(self):
        sök_kriterie = datetime.now().strftime("%Y%m%d")
        matchande_kvitton = self.kvitto._sök_kvitto(sök_kriterie)
        if matchande_kvitton:
            for matchande_kvitto in matchande_kvitton:
                print(matchande_kvitto)
    
    def sök_datum_kvitto(self):
        sök_kriterie = self.universal_input_hantering(
            "Ange datum (YYYYMMDD): ")
        matchande_kvitton = self.kvitto._sök_kvitto(sök_kriterie)
        if matchande_kvitton:
            for matchande_kvitto in matchande_kvitton:
                print(matchande_kvitto)
                
    def produkt_meny(self):
        self.submeny_hanterare('produkt')

    def lägg_till_vara(self):
        try:
            produkt_id = self.universal_input_hantering(
                "Välj id för produkten mellan 100-999: ", 
                input_type=int, min_värde=100, max_värde=999)
            produkt_namn = self.universal_input_hantering(
                "Välj ett namn för produkten: ")
            produkt_pris = self.universal_input_hantering(
                "Välj ett pris på varan: ", input_type=float)
            self.lager.lägg_till_produkt(produkt_id, produkt_namn, produkt_pris)
            print(f"Produkten {produkt_namn} har lagts till med id {produkt_id}")
        except ExitSubmenuException:
            return
        except ValueError:
            print("Error: Välj ett positivt pris tack")

    def ta_bort_vara(self):
        produkt_id = self.universal_input_hantering(
            "Vad är ID på produkten du vill ta bort?: ")
        self.lager.ta_bort_produkt(produkt_id)

    def visa_varulager(self):
        print(self.lager.visa_produkt_lager())

    def uppdatera_vara(self):
        self.submeny_hanterare('uppdatera_produkt')

    def uppdatera_produkt_namn(self):
        produkt_id = self.universal_input_hantering(
            "Ange produktid för varan du vill uppdatera: ")
        nytt_namn = self.universal_input_hantering(
            "Ange nytt namn för varan: ")
        self.lager.uppdatera_produkt(produkt_id,'name', nytt_namn)

    def uppdatera_produkt_pris(self):
        produkt_id = self.universal_input_hantering(
            "Ange produktid för varan du vill uppdatera: ")
        nytt_pris = self.universal_input_hantering(
            "Ange nytt pris för varan: ", input_type=float)
        self.lager.uppdatera_produkt(produkt_id,'pris', nytt_pris)
    
    def kampanj_meny(self):
        self.submeny_hanterare('kampanj')

    def ny_kampanj(self):
        produkt = self.universal_input_hantering(
            "Skriv produktid för produkten du ha på kampanj\n: ")
        produkt = self.lager.sök_efter_produkt(produkt)
        if not produkt:
            print("Produkten finns inte, försök igen")
            return
        kampanj_namn = self.universal_input_hantering(
            "Vad ska kampanjen heta: ").capitalize()
        try:
            kampanj_pris = self.universal_input_hantering(
                "Mata in nya kampanj priset: ", input_type=float)
            kampanj_start_datum, kampanj_slut_datum = self.lager.skapa_kampanj_datum()
        except ValueError:
            print("Felaktig pris. Vänligen mata in ett numeriskt värde")
        self.lager.lägg_till_kampanj(produkt.produkt_id, kampanj_namn, kampanj_pris,\
                                     kampanj_start_datum, kampanj_slut_datum)
        
    def ta_bort_kampanj(self):
        self.visa_kampanj_lager()
        produkt_id = self.universal_input_hantering(
            "Ange produktid för produkten vars kampanj du vill ta bort: ")
        kampanj_namn = self.universal_input_hantering(
            "Ange namn på kampanjen du vill ta bort: ")
        self.lager.ta_bort_kampanj(produkt_id, kampanj_namn)

    def uppdatera_kampanj(self):
        produkt_id = self.universal_input_hantering(
            "Ange produktid för att se vilka kampanjer produkten har: ")
        kampanjer = self.lager.visa_kampanjer_för_produkt(produkt_id)
        if not kampanjer:
            print("Finns ingen kampanj att uppdatera för produkten")
            return
        val_kampanj_index = self.universal_input_hantering(
            "Ange numret på kampanjen som du vill ändra: ", input_type=int) - 1 #eftersom 0 går tillbaka är detta en workaround  # noqa: E501
        if 0 <= val_kampanj_index < len(kampanjer):
            val_kampanj = kampanjer[val_kampanj_index]
            self.submeny_hanterare('uppdatera_kampanj', produkt_id, val_kampanj)
        else:
            print("Ogiltigt val av kampanj")

    def uppdatera_kampanj_namn(self, produkt_id, kampanj_namn):
        nytt_namn = self.universal_input_hantering(
            f"Välj det nya namnet för kampanjen {kampanj_namn}: ")
        self.lager.uppdatera_kampanj(produkt_id, kampanj_namn, nytt_namn)

    def uppdatera_kampanj_pris(self, produkt_id, kampanj_namn):
        nytt_pris = float(self.universal_input_hantering(
            f"Välj det nya priset för kampanjen {kampanj_namn}: ", input_type=float))
        if nytt_pris <= 0:
            print("Priset måste vara positivt")
            return
        self.lager.uppdatera_kampanj(produkt_id, kampanj_namn, nytt_pris=nytt_pris)

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
                self.kvitto.lägg_till(namn, int(antal), float(belopp), 
                                          kampanj_start_datum, kampanj_slut_datum)

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
    lager.ladda_produkt_och_kampanj()
    kvitto.öppna_kvitto_nummer()
    admin_meny = Administrera(lager, kvitto)
    lager.ladda_meny_och_funktion_hanterare(admin_meny)
    admin_meny.main()

if __name__ == "__main__":
    uppstart()
