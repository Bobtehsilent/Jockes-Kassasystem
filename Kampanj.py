from datetime import datetime
class Kampanj:
    def __init__(self, kampanj_namn, produkt_namn, kampanj_pris, kampanj_start_datum, kampanj_slut_datum):
        self.__kampanj_namn = kampanj_namn
        self.__produkt_namn = produkt_namn
        self.__kampanj_Pris = kampanj_pris
        self.__kampanj_Start_Datum = kampanj_start_datum
        self.__kampanj_Slut_Datum = kampanj_slut_datum
        if kampanj_pris <= 0:
            raise ValueError("Kampanj priset måste vara positivt")

    @property
    def kampanj_namn(self):
        return self.__kampanj_namn

    @kampanj_namn.setter
    def kampanj_namn(self, nytt_kampanj_namn):
        self.__kampanj_namn = nytt_kampanj_namn

    @property
    def produkt_namn(self):
        return self.__produkt_namn

    @produkt_namn.setter
    def produkt_namn(self, nytt_produkt_namn):
        self.__produkt_namn = nytt_produkt_namn

    @property
    def kampanj_pris(self):
        return self.__kampanj_Pris

    @kampanj_pris.setter
    def kampanj_pris(self, nytt_kampanj_pris):
        self.__kampanj_Pris = nytt_kampanj_pris

    @property
    def kampanj_start_datum(self):
        return self.__kampanj_Start_Datum

    @kampanj_start_datum.setter
    def kampanj_start_datum(self, nytt_start_datum):
        self.__kampanj_Start_Datum = nytt_start_datum

    @property
    def kampanj_slut_datum(self):
        return self.__kampanj_Slut_Datum

    @kampanj_slut_datum.setter
    def kampanj_slut_datum(self, nytt_slut_datum):
        self.__kampanj_Slut_Datum = nytt_slut_datum

    def är_aktiv(self):
        idag = datetime.today()
        return self.kampanj_start_datum <= idag <= self.kampanj_slut_datum

    def kampanjdagar_kvar(self):
        if self.är_aktiv():
            dagar_kvar = (self.kampanj_slut_datum - datetime.today()).days
            return dagar_kvar
        else:
            return 0

    def räkna_rabatt(self, original_pris):
        return original_pris * (1 - (self.kampanj_pris // 100))

    def formattera(self):
        return {
            'kampanj_namn': self.kampanj_namn,
            'produkt_namn': self.produkt_namn,
            'kampanj_pris': self.kampanj_pris,
            'kampanj_start_datum': self.kampanj_start_datum,
            'kampanj_slut_datum': self.kampanj_slut_datum
        }

    def __str__(self):
        return f"Startdatum: {self.kampanj_start_datum} Slutdatum: {self.kampanj_slut_datum} kampanjpris: {self.kampanj_pris}"
