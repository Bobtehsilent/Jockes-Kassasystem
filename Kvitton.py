from datetime import datetime
from Produkter import Produkt

class KvittoRad:
    def __init__(self, produkt_namn:str, count:int, per_pris:float, kampanj_datum:str, kampanj_pris:float):  # noqa: E501
        self.__produkt_namn = produkt_namn
        self.__count = count
        self.__per_pris = per_pris
        self.__kampanj_datum = kampanj_datum
        self.__kampanj_pris = kampanj_pris
    def Add_count(self,count):
         self.__count = self.__count + count
    def Get_Total(self):
        return self.__count * self.__per_pris
    def Get_Name(self):
        return self.__produkt_namn
    def Get_Count(self):
        return self.__count
    def Get_Per_Pris(self):
        return self.__per_pris
    def Get_Kampanj_datum(self):
        return self.__kampanj_datum
    def Get_Kampanj_Pris(self):
        return self.__kampanj_pris
    def Get_Total_kampanj(self):
        return self.__count * self.__kampanj_pris
    def set_pris(self, new_price):
        self.__per_pris = new_price

class Kvitto:
    def __init__(self) -> None:
        self.__datum = datetime.now().date()
        self.__kvitto_rad = []
        self.__nuvarande_kvitto_nummer = 0
    def Get_kvitto_nummer(self):
        return self.__nuvarande_kvitto_nummer
    def set_kvitto_nummer(self, nummer):
        self.__nuvarande_kvitto_nummer = nummer
    def Generera_kvitto(self):
        datum_nu = self.__datum
        datum_nu = datum_nu.strftime("%Y%m%d")
        self.__nuvarande_kvitto_nummer += 1
        kvitto_text = f"\nKvitto Nummer: {self.__nuvarande_kvitto_nummer}\n"
        for item in self.__kvitto_rad:
            kvitto_text += f"{item.Get_Name()}: {item.Get_Count()} x {item.Get_Per_Pris()} = {item.Get_Total()}\n"
        kvitto_text += "\n" + "*" * 40 + "\n"
        with open(f"RECEIPT_{datum_nu}.txt", "a") as kvitto_fil:
            kvitto_fil.write(kvitto_text)
        return self.__nuvarande_kvitto_nummer

    def Total_Summa(self):
        total = 0
        for row in self.__kvitto_rad:
            total = total + row.Get_Total()
        return total
    def Get_Datum(self):
        return self.__datum
    
    def Lägg_Till(self, produkt_namn:str, count:int, per_pris:float, kampanj_datum:str, kampanj_pris:float):
        kvitto_rad = KvittoRad(produkt_namn, count, per_pris , kampanj_datum, kampanj_pris)
        for prdukt in self.__kvitto_rad:
            if prdukt.Get_Name() == kvitto_rad.Get_Name():
                prdukt.Add_count(count)
                return
        if kampanj_datum and "," in kampanj_datum:
            parts = kampanj_datum.split(",")
            print(parts)
            start = datetime.strptime(parts[0],"%Y-%m-%d").date()
            end = datetime.strptime(parts[1],"%Y-%m-%d").date()
            current_date = datetime.now().date()
            print("Lägger till kampanjpris")
            if start <= current_date <= end:
                kvitto_rad.set_pris(kampanj_pris)
        self.__kvitto_rad.append(kvitto_rad)

    def Get_Kvittorad(self):
        return self.__kvitto_rad
    def Kolla_Kampanj_Inom_Datum(self, getDatum1, getDatum2):
        start = datetime.strptime(getDatum1,"%Y-%m-%d").date()
        end = datetime.strptime(getDatum2,"%Y-%m-%d").date()
        currentDatum = datetime.now().date()
        if start <= currentDatum <= end:
            return True
        return False
    def Sök_kvitto(self, sök_kriterie):
        try:
            with open("AllaKvitton.txt", "r") as kvitto_fil:
                alla_kvitton = kvitto_fil.read()
            kvitton = alla_kvitton.split("\n" + "*" * 40 + "\n")
            matchande_kvitton = []
            for kvitto in kvitton:
                if sök_kriterie in kvitto:
                    matchande_kvitton.append(kvitto)
            return matchande_kvitton
        except FileNotFoundError:
            print("Error: Inga kvitton hittades.")
    def Skriv_kvitto(self):
        print(f"Kvitto {self.Get_Datum()}")
        for rad in self.__kvitto_rad:
            produkt_namn = rad.Get_Name()
            count = rad.Get_Count()
            per_pris = rad.Get_Per_Pris()
            kampanj_datum = rad.Get_Kampanj_datum()
            if kampanj_datum is not None:
                print(f"{produkt_namn} x {count} (Kampanjpris: {per_pris} SEK)")
            else:
                print(f"{produkt_namn} x {count} (Pris: {per_pris} SEK)")
            
        total_summa = self.Total_Summa()
        print(f"Total summa: {total_summa} SEK")