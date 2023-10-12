from datetime import datetime
import json
import os
from Lager import Lager
from Kvitton import Kvitto

def val_hantering(prompt,min_värde, max_värde):
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
def delade():
    while True:
        kassa_input = input("Kommando: ")
        delar = kassa_input.split(' ')
        if len(delar) == 2:
            return delar[0], delar[1]
        elif len(delar) == 1:
            if delar[0].lower() == "pay" or delar[0].lower() == 'q':
                return delar
        print("För få tecken inskrivna, försök igen")
def admin_meny():
    print("1. Sök kvitto\n2. Produktmeny\n3. Kampanjmeny\n4. Stäng ner Administration")
    val_för_admin_menyn = val_hantering((":"), min_värde=1, max_värde=4)
    return val_för_admin_menyn
def admin_meny_val():
    while True:
        val_för_admin_menyn = admin_meny()
        if val_för_admin_menyn == 1:
            while True:
                print("1. Kvittot har dagens datum\n2. Välj ett datum att söka efter\n3. Gå tillbaka")
                val_för_sök_kvitto = val_hantering((":"), min_värde=1,max_värde=3)
                if val_för_sök_kvitto == 1:
                    sök_kriterie = datetime.now().strftime("%Y-%m-%d")
                    break
                elif val_för_sök_kvitto == 2:
                    sök_kriterie = input("Ange datum (YYYY-MM-DD): ")
                    break
                elif val_för_sök_kvitto == 3:
                    break
            matchande_kvitton = kvitto.sök_kvitto(sök_kriterie)
            if matchande_kvitton:
                for matchande_kvitto in matchande_kvitton:
                    print(matchande_kvitto)
            else:
                print("Fanns inga kvitton för angivna datumet.")
        if val_för_admin_menyn == 2:
            produkt_meny()
        if val_för_admin_menyn == 3:
            kampanj_meny()
        if val_för_admin_menyn == 4:
            break
def produkt_meny():
    while True:
        print("1. Lägg till produkt\n2. Ta bort produkt\n3. Visa lager\n4. Uppdatera existerande produkt\n5. Tillbaka till Administraion")
        val_för_produkt_meny = val_hantering((":"), min_värde=1, max_värde=5)
        if val_för_produkt_meny == 1:
            produkt_id = input("Välj id för produkten: ")
            produkt_namn = input("Välj ett namn för produkten: ")
            try:
                produkt_pris = float(input("Välj ett pris på varan: "))
            except ValueError:
                print("Error: Välj ett positivt pris tack")
                continue
            lager.lägg_till_produkt(produkt_id, produkt_namn, produkt_pris)
            print(f"Produkten {produkt_namn} har lagts till med id {produkt_id}")
        elif val_för_produkt_meny == 2:
            produkt_id = input("Vad är ID på produkten du vill ta bort?: ")
            lager.ta_bort_produkt(produkt_id)
        elif val_för_produkt_meny == 3:
            print(lager.visa_lager())
        elif val_för_produkt_meny == 4:
            print("1.Uppdatera Namn\n2.Uppdatera Pris")
            val_uppdatera = val_hantering(":", min_värde=1,max_värde=2)
            if val_uppdatera == 1:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                nytt_namn = input("Ange nytt namn för varan: ")
                lager.uppdatera_produkt(produkt_id,'name', nytt_namn)
            elif val_uppdatera == 2:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                try:
                    nytt_pris = int(input("Ange nytt pris för varan (Positivt heltal): "))
                except ValueError:
                    print("Error: Ange ett positivt heltal.")
                lager.uppdatera_produkt(produkt_id,'pris', nytt_pris)
        elif val_för_produkt_meny == 5:
            lager.spara_filer()
            break
def kampanj_meny():
    while True:
        print("1. Lägg till kampanj\n2. Ta bort kampanj\n3. Uppdatera existerande kampanj\n4. Visa lager\n5. Tillbaka till Administraion")
        val_för_kampanj_meny = val_hantering((":"), min_värde=1, max_värde=5)
        if val_för_kampanj_meny == 1:
            produkt = input("Skriv produktid på produkten du vill ha på kampanj(Q för att gå tillbaka): ")
            if produkt.lower() == "q":
                break
            else:
                hitta_produkt = lager.sök_efter_produkt(produkt)
                if not hitta_produkt:
                    print("Produkten finns inte, försök igen")
                    continue
                kampanj_namn = input("Vad ska kampanjen heta?: ")
                try:
                    kampanj_pris = float(input("Mata in nya kampanj priset: "))
                    kampanj_start_datum, kampanj_slut_datum = lager.skapa_kampanj_datum()
                except ValueError:
                    print("Felaktig pris. Vänligen mata in ett numeriskt värde")
                lager.lägg_till_kampanj(produkt, kampanj_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum)
        elif val_för_kampanj_meny == 2:
            kampanj_namn = input("Ange namn på kampanjen du vill ta bort: ")
            lager.ta_bort_kampanj(kampanj_namn)
        elif val_för_kampanj_meny == 3:
            kampanj_namn = input("Ange namn på kampanjen du vill uppdatera: ")
            try:
                nytt_pris = float(input("Ange det nya kampanjpriset(Positivt heltal): "))
            except ValueError:
                print("Error: Ange ett positivt heltal.")
            lager.uppdatera_kampanj(kampanj_namn, nytt_pris)
        elif val_för_kampanj_meny == 4:
            print(lager.visa_lager())
            continue
        elif val_för_kampanj_meny == 5:
            break
def nytt_kvitto():
    kvitto.kvitto_nummer += 1
    while True:
        print("Kassa 1")
        print("Kommandon:")
        print("<produktid> <Space> <antal>")
        print("PAY")
        print("Gå tillbaka: Q")
        delar = delade()
        if not delar:
            print("Ogiltigt kommando. Försök igen")
            continue
        elif delar[0].lower() == 'q':
            break
        elif delar[0].lower() == 'pay':
            kvitto_nummer = kvitto.generera_kvitto()
            kvitto.skriv_kvitto()
            print(f"Kvitto {kvitto_nummer} har genererats.")
            kvitto.resetta_kvitto()
            break
        else:
            produkt_id = delar[0]
            antal = delar[1]
            try:
                namn, belopp, kampanj_start_datum, kampanj_slut_datum = lager.hämta_produkt_info(produkt_id)
            except IndexError:
                print("Error: produkt informationen är ej komplett")
            except Exception as e:
                print(f"Error: {e}")
                continue
            try:
                kvitto.lägg_Till(namn, int(antal), float(belopp), kampanj_start_datum, kampanj_slut_datum)
            except ValueError:
                print("Mata in enligt formatet <Produktid> <Antal> eller PAY")
            kvitto.skriv_kvitto()

        
def print_main_meny():
    print("1. Ny kund")
    print("2. Administration")
    print("0. Avsluta")
    val_huvud_meny = val_hantering((":"), min_värde=0, max_värde=2)
    return val_huvud_meny
def main():
    while True:
        val_main = print_main_meny()
        if val_main == 0:
            lager.spara_filer()
            break
        elif val_main == 1:
            nytt_kvitto()
            print(kvitto.kvitto_nummer)
        elif val_main == 2:
            admin_meny_val()


if __name__ == "__main__":
    kvitto = Kvitto()
    lager = Lager()
    if not os.path.isfile("produkt_och_kampanj.json"):
        default_data = {'produkter': [], 'kampanjer': []}
        with open("produkt_och_kampanj.json", "a") as f:    
            json.dump(default_data, f)
    lager.öppna_filer()
    kvitto.öppna_kvitto_nummer()
    print(lager.produkter)
    print(lager.kampanjer)

    main()
    