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

    def val_hantering(self, prompt,min_värde, max_värde):
        while True:
            try:
                val = int(input(prompt))
                if val < min_värde or val > max_värde:
                    print(f"Mata in ett tal mellan {min_värde} och {max_värde} tack")
                else:
                    break
            except ValueError:
                print(f"Error: Mata in ett tal mellan {min_värde} och {max_värde}")
                continue
        return val
    
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
        return self.val_hantering(":", min_värde=0, max_värde=max_val)
    
    def sök_kvitto_meny(self):
        while True:
            val_för_sök_kvitto = self.print_meny('kvitto')
            if val_för_sök_kvitto == 1:
                sök_kriterie = datetime.now().strftime("%Y-%m-%d")
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
        while True:
            meny_val = self.print_meny('produkt')
            if meny_val == 1:
                self.lägg_till_vara()
            elif meny_val == 2:
                self.ta_bort_vara()
            elif meny_val == 3:
                self.visa_varulager()
            elif meny_val == 4:
                self.uppdatera_vara()
            elif meny_val == 0:
                break

    def lägg_till_vara(self):
        try:
            produkt_id = input("Välj id för produkten: ")
            self.gå_tillbaka_subval(produkt_id)
            produkt_namn = input("Välj ett namn för produkten: ")
            self.gå_tillbaka_subval(produkt_namn)
            produkt_pris = float(input("Välj ett pris på varan: "))
            self.gå_tillbaka_subval(produkt_pris)
            self.lager.lägg_till_produkt(produkt_id, produkt_namn, produkt_pris)
            print(f"Produkten {produkt_namn} har lagts till med id {produkt_id}")
        except ExitSubmenuException:
            return
        except ValueError:
            print("Error: Välj ett positivt pris tack")

    def ta_bort_vara(self):
        produkt_id = input("Vad är ID på produkten du vill ta bort?: ")
        self.gå_tillbaka_subval(produkt_id)
        self.lager.ta_bort_produkt(produkt_id)

    def visa_varulager(self):
        print(self.lager.visa_produkt_lager())

    def uppdatera_vara(self):
        try:
            val_uppdatera = self.print_meny('uppdatera')
            if val_uppdatera == 1:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                self.gå_tillbaka_subval(produkt_id)
                nytt_namn = input("Ange nytt namn för varan: ")
                self.gå_tillbaka_subval(nytt_namn)
                self.lager.uppdatera_produkt(produkt_id,'name', nytt_namn)
            elif val_uppdatera == 2:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                self.gå_tillbaka_subval(produkt_id)
                nytt_pris = int(input("Ange nytt pris för varan: "))
                self.gå_tillbaka_subval(nytt_pris)
                self.lager.uppdatera_produkt(produkt_id,'pris', nytt_pris)
        except ValueError:
            print("Error: Ange ett positivt heltal.")
    
    def kampanj_meny(self):
        while True:
            meny_val = self.print_meny('kampanj')
            if meny_val == 1:
                self.ny_kampanj()
            elif meny_val == 2:
                self.ta_bort_kampanj()
            elif meny_val == 3:
                self.uppdatera_kampanj()
            elif meny_val == 4:
                print(self.lager.visa_kampanj_lager())
            elif meny_val == 0:
                break

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
        while True:
            meny_val = self.print_meny('admin')
            if meny_val == 1:
                self.sök_kvitto_meny()
            if meny_val == 2:
                self.produkt_meny()
            if meny_val == 3:
                self.kampanj_meny()
            if meny_val == 0:
                break
    
    def main(self):
        while True:
            val_main = self.print_meny('main')
            if val_main == 0:
                self.lager.spara_filer()
                break
            elif val_main == 1:
                self.nytt_kvitto()
            elif val_main == 2:
                self.admin_meny_val()
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
