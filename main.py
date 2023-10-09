from datetime import datetime
import os
from Lager import Lager
from Kvitton import Kvitto

def ValHantering(prompt,min_värde, max_värde):
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
            if delar[0].lower() == "pay":
                return delar
        print("För få tecken inskrivna, försök igen")
def Admin_meny():
    print("1. Sök kvitto\n2. Produktmeny\n3. Kampanjmeny\n4. Stäng ner Administration")
    val_för_admin_menyn = ValHantering((":"), min_värde=1, max_värde=4)
    return val_för_admin_menyn
def Admin_meny_val():
    while True:
        val_för_admin_menyn = Admin_meny()
        if val_för_admin_menyn == 1:
            sök_kriterie = input("Vilket datum har kvittot du söker?: ")
            kvitto.Sök_kvitto(sök_kriterie)
        if val_för_admin_menyn == 2:
            produkt_meny()
        if val_för_admin_menyn == 3:
            kampanj_meny()
        if val_för_admin_menyn == 4:
            break
def produkt_meny():
    while True:
        print("1. Lägg till produkt\n2. Ta bort produkt\n3. Visa lager\n4. Uppdatera existerande produkt\n5. Tillbaka till Administraion")
        val_för_produkt_meny = ValHantering((":"), min_värde=1, max_värde=5)
        if val_för_produkt_meny == 1:
            produkt_id = input("Välj id för produkten: ")
            produkt_namn = input("Välj ett namn för produkten: ")
            try:
                produkt_pris = float(input("Välj ett pris på varan: "))
            except ValueError:
                print("Error: Välj ett positivt pris tack")
                continue
            lager.lägg_till_produkt(produkt_id, produkt_namn, produkt_pris)
            lager.spara_filer("produkt_och_kampanj.json")
        elif val_för_produkt_meny == 2:
            produkt_id = input("Vad är ID på produkten du vill ta bort?: ")
            lager.ta_bort_produkt(produkt_id)
        elif val_för_produkt_meny == 3:
            lager.visa_lager()
        elif val_för_produkt_meny == 4:
            print("1.Uppdatera Namn\n2.Uppdatera Pris")
            val_uppdatera = ValHantering(":", min_värde=1,max_värde=2)
            if val_uppdatera == 1:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                nytt_namn = input("Ange nytt namn för varan: ")
                lager.uppdatera_produkt_namn(produkt_id, nytt_namn)
            elif val_uppdatera == 2:
                produkt_id = input("Ange produktid för varan du vill uppdatera: ")
                try:
                    nytt_pris = int(input("Ange nytt pris för varan (Positivt heltal): "))
                except ValueError:
                    print("Error: Ange ett positivt heltal.")
                lager.uppdatera_produkt_pris(produkt_id, nytt_pris)
        elif val_för_produkt_meny == 5:
            break
def kampanj_meny():
    print("1. Lägg till kampanj\n2. Ta bort kampanj\n3. Uppdatera existerande kampanj\n4. Tillbaka till Administraion")
    while True:
        val_för_kampanj_meny = ValHantering((":"), min_värde=1, max_värde=4)
        if val_för_kampanj_meny == 1:
            lager.visa_lager()
            produkt = input("Skriv namnet på produkten du vill ha på kampanj: ")
            hitta_produkt = lager.sök_efter_produkt(produkt)
            if not hitta_produkt:
                print("Produkten finns inte, försök igen")
                continue
            kampanj_namn = input("Vad ska kampanjen heta?: ")
            kampanj_pris = float(input("Mata in nya kampanj priset: "))
            lager.lägg_till_kampanj(produkt, kampanj_namn, kampanj_pris)
            lager.spara_filer("produkt_och_kampanj.json")
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
            break
def nytt_kvitto():
    kvitto = Kvitto()
    while True:
        print("Kassa")
        print("Kommandon:")
        print("<produktid> <Space> <antal>")
        print("PAY")
        delar = delade()
        if not delar:
            print("Ogiltigt kommando. Försök igen")
            continue
        elif delar[0].lower() == 'pay':
            kvitto_nummer = kvitto.Generera_kvitto()
            kvitto.Skriv_kvitto()
            print(f"Kvitto {kvitto_nummer} har genererats.")
            break
        else:
            produkt_id = delar[0]
            antal = delar[1]
            hitta_produkter = lager.hämta_produkt_info(produkt_id)
            if hitta_produkter is None:
                print("Produkten finns inte, Försök igen")
                continue
            namn = hitta_produkter[0]
            belopp = hitta_produkter[1]
            kampanj_datum = hitta_produkter[2]
            kampanj_pris = hitta_produkter[3]
            try:
                kvitto.Lägg_Till(namn,int(antal),float(belopp),kampanj_datum, kampanj_pris)
            except ValueError:
                print("Mata in enligt formatet <Produktid> <Antal> eller PAY")
            kvitto.Skriv_kvitto()

        
def print_main_meny():
    print("1. Ny kund")
    print("2. Administration")
    print("0. Avsluta")
    val_huvud_meny = ValHantering((":"), min_värde=0, max_värde=2)
    return val_huvud_meny
def main():
    while True:
        val_main = print_main_meny()
        if val_main == 0:
            break
        elif val_main == 1:
            nytt_kvitto()
        elif val_main == 2:
            Admin_meny_val()


if __name__ == "__main__":
    kvitto = Kvitto()
    lager = Lager()
    if not os.path.isfile("produkt_och_kampanj.json"):
        with open("produkt_och_kampanj.json", "a") as f:    
            pass
    lager.öppna_filer("produkt_och_kampanj.json")
    print(lager.produkter)
    print(lager.kampanjer)

    main()
    