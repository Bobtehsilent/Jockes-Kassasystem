from datetime import datetime

class KvittoRad:
    def __init__(self, produkt_namn:str, count:int, per_pris:float, 
                 kampanj_start_datum=None, kampanj_slut_datum=None, kampanj_pris=None):
        self.__produkt_namn = produkt_namn
        self.__count = count
        self.__per_pris = per_pris
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
    
    @per_pris.setter
    def per_pris(self, nytt_pris):
        self.__per_pris = nytt_pris

    @property
    def kampanj_pris(self):
        if self.__kampanj_pris is not None and self.kampanj_är_aktiv:
            return self.__kampanj_pris
        return None
    
    @property
    def kampanj_är_aktiv(self):
        if self.__kampanj_start_datum and self.__kampanj_slut_datum:
            nuvarande_datum = datetime.now().date()
            kampanj_start_datum = self.__kampanj_start_datum.date()
            kampanj_slut_datum = self.__kampanj_slut_datum.date()
            return kampanj_start_datum <= nuvarande_datum <= kampanj_slut_datum
        return False

class Kvitto:
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
    
    def _sök_kvitto(self, sök_kriterie):
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
    
    def generera_kvitto(self):
        datum_nu = self.datum.strftime("%Y%m%d")
        kvitto_text = f"\nKvitto: {self.kvitto_nummer} : {datum_nu}\n"
        for item in self.kvitto_rad:
            kvitto_text += f"{item.produkt_namn}: {item.count} x "
            f"{'(Kampanjpris)' if item.kampanj_är_aktiv else ''}:"
            f"{item.per_pris} SEK each = {item.total:.2f}\n"
        kvitto_text += f"\nTotal summa: {self.total_summa():.2f} SEK\n" +"*"* 40 + "\n"
        with open(f"RECEIPT_{datum_nu}.txt", "a") as kvitto_fil:
            kvitto_fil.write(kvitto_text)
        return self.kvitto_nummer
    
    def skriv_kvitto_rad(self, rad):
        print(f"{rad.produkt_namn}: {rad.count} x {rad.per_pris}: {rad.total:.2f}"
                  f" SEK {'(Kampanjpris)' if rad.kampanj_är_aktiv else ''}")

    def skriv_kvitto(self):
        print(f"Kvitto: {self.kvitto_nummer} | {self.datum.date()}")
        for rad in self.kvitto_rad:
            self.skriv_kvitto_rad(rad)
        print(f"Total summa: {self.total_summa():.2f} SEK\n")

    def öppna_kvitto_nummer(self):
        try:
            datum_nu = self.datum.strftime("%Y%m%d")
            max_kvitto_nummer = 0
            with open(f"RECEIPT_{datum_nu}.txt", "r") as f:
                for line in f:
                    if line.startswith("Kvitto:"):
                        kvitto_nummer = int(line.split()[1])
                        max_kvitto_nummer = max(max_kvitto_nummer, kvitto_nummer)
            self.kvitto_nummer = max_kvitto_nummer
        except FileNotFoundError:
            print(f"Ingen aktuell kvittofil. Öppnar en ny för: {datum_nu}")