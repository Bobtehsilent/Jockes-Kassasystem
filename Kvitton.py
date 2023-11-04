from datetime import datetime

class KvittoRad: #skapar objekten för varje rad för kvittot
    def __init__(self, produkt_namn:str, count:int, per_pris:float, pris_typ:str, 
                 kampanj_start_datum=None, kampanj_slut_datum=None, kampanj_pris=None):
        self.__produkt_namn = produkt_namn
        self.__count = count
        self.__per_pris = per_pris
        self.__pris_typ = pris_typ
        self.__kampanj_start_datum = kampanj_start_datum
        self.__kampanj_slut_datum = kampanj_slut_datum
        self.__kampanj_pris = kampanj_pris

    def add_count(self,count):
         self.__count = self.__count + count

    @property
    def total(self):
        aktivt_pris = self.kampanj_pris if self.kampanj_pris and self.kampanj_är_aktiv \
                        else self.per_pris
        return self.__count * aktivt_pris
    
    @property
    def produkt_namn(self):
        return self.__produkt_namn
    
    @property
    def count(self):
        return self.__count
    
    @property
    def per_pris(self):
        return self.__per_pris
    
    @property
    def pris_typ(self):
        return self.__pris_typ

    @property
    def kampanj_pris(self):
        if self.__kampanj_pris is not None and self.kampanj_är_aktiv:
            return self.__kampanj_pris
        return None
    
    @property #kollar om en kampanj är aktuell.
    def kampanj_är_aktiv(self):
        if self.__kampanj_start_datum and self.__kampanj_slut_datum:
            nuvarande_datum = datetime.now().date()
            kampanj_start_datum = self.__kampanj_start_datum.date()
            kampanj_slut_datum = self.__kampanj_slut_datum.date()
            return kampanj_start_datum <= nuvarande_datum <= kampanj_slut_datum
        return False

class Kvitto: #Funktionalitet för att skapa kvitton och hålla koll på kvittonummer
    def __init__(self) -> None:
        self.__datum = datetime.now()
        self.kvitto_rad = []
        self.__nuvarande_kvitto_nummer = 0
        
    @property
    def kvitto_nummer(self):
        return self.__nuvarande_kvitto_nummer
    
    @kvitto_nummer.setter
    def kvitto_nummer(self, nummer):
        self.__nuvarande_kvitto_nummer = nummer

    @property
    def datum(self):
        return self.__datum
    
    def resetta_kvitto(self):
        self.kvitto_rad = []

    def total_summa(self):
        return sum(item.total for item in self.kvitto_rad)
    
    #Funktion för att lägga till varor i kvittot och sedan printa ut, används vid "shopping"
    def lägg_till(self, produkt_namn:str, count:int, per_pris:float, 
                  kampanj_start_datum=None, kampanj_slut_datum=None, kampanj_pris=None):
        for produkt in self.kvitto_rad:
            if produkt.produkt_namn == produkt_namn:
                produkt.add_count(count)
                break
        else:
            kvitto_rad = KvittoRad(produkt_namn, count, per_pris , kampanj_start_datum,
                                    kampanj_slut_datum, kampanj_pris)
            self.kvitto_rad.append(kvitto_rad)
        for rad in self.kvitto_rad:
            self.skriv_kvitto_rad(rad)
    
    def sök_kvitto(self, sök_kriterie): #Söker kvitto efter valt datum och returnerar en lista med alla kvitton.
        matchande_kvitton = []
        try:
            with open(f"RECEIPT_{sök_kriterie}.txt", "r") as kvitto_fil:
                alla_kvitton = kvitto_fil.read()
            kvitton = alla_kvitton.split("\n" + "*" * 40 + "\n")
            for kvitto in kvitton:
                if sök_kriterie in kvitto:
                    matchande_kvitton.append(kvitto)
                    matchande_kvitton.append("\n")
        except FileNotFoundError:
            print("Error: Inga kvitton hittades.")
        return matchande_kvitton
    
    def generera_kvitto(self): #Aktiveras av att betalaa (pay). Skapar/lägger till i kvitto textfil samt uppdaterar kvittonummer fil
        datum_för_txt = self.datum.strftime("%Y%m%d")
        datum_för_rad = self.datum.strftime("%Y-%m-%d %H:%M")
        kvitto_text = f"\nKvitto: {self.kvitto_nummer} : {datum_för_rad}\n"
        for item in self.kvitto_rad:
            kvitto_text += (f"{item.produkt_namn}: {item.count} * "
                            f"{item.per_pris}/{item.pris_typ} each = {item.total:.2f}"
                            f"{'(Kampanjpris)' if item.kampanj_är_aktiv else ''}\n")
        kvitto_text += f"\nTotal summa: {self.total_summa():.2f} SEK\n" +"*"* 40 + "\n"
        with open(f"RECEIPT_{datum_för_txt}.txt", "a") as kvitto_fil:
            kvitto_fil.write(kvitto_text)
        with open('Kvittonummer.txt', 'w') as kvittonummer_fil:
            kvittonummer_fil.write(str(self.kvitto_nummer))
        return self.kvitto_nummer
    
    def skriv_kvitto_rad(self, rad):
        print(f"{rad.produkt_namn}: {rad.count} * {rad.per_pris}/{rad.pris_typ}: {rad.total:.2f}"
                  f" SEK {'(Kampanjpris)' if rad.kampanj_är_aktiv else ''}")

    def skriv_kvitto(self): #Skriver ut nuvarande kvitto efter varje gång man lägger till en vara (during shopping)
        datum_för_rad = self.datum.strftime("%Y-%m-%d %H:%M")
        print(f"Kvitto: {self.kvitto_nummer} | {datum_för_rad}")
        for rad in self.kvitto_rad:
            self.skriv_kvitto_rad(rad)
        print(f"Total summa: {self.total_summa():.2f} SEK\n")

    def öppna_kvitto_nummer(self):
        with open('Kvittonummer.txt', 'r') as kvittonummer_fil:
            nuvarande_kvitto_nummer = int(kvittonummer_fil.read().strip())
        self.kvitto_nummer = nuvarande_kvitto_nummer
