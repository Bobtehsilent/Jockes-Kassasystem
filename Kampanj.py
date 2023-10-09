# c. Discount Campaigns (Class: DiscountCampaign)
  # - Create a class to handle discount campaigns.
   #- Include attributes like campaign name, discount percentage, applicable products, and expiration date.
   #- Implement methods for creating and managing discount campaigns.
from datetime import datetime
class Kampanj:
    def __init__(self, kampanj_namn, kampanj_pris, kampanj_Start_Datum, kampanj_Slut_Datum):
        self.__kampanj_namn = kampanj_namn
        self.__kampanj_Pris = kampanj_pris
        self.__kampanj_Start_Datum = datetime.strptime(kampanj_Start_Datum, '%Y-%m-%d')
        self.__kampanj_Slut_Datum = datetime.strptime(kampanj_Slut_Datum, '%Y-%m-%d')
        if kampanj_pris <= 0:
            raise ValueError("Kampanj priset måste vara positivt")
        if self.__kampanj_Start_Datum >= self.__kampanj_Slut_Datum:
            raise ValueError("Kampanjen måste ta slut efter startdatumet")
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
    def formatera(self):
        return {
            'kampanjPris' : self.kampanj_pris,
            'kampanjStartDatum': self.kampanj_start_datum,
            'kampanjSlutDatum' : self.kampanj_slut_datum
        }
    def __str__(self):
        return f"StartDatum: {self.kampanj_start_datum} SlutDatum: {self.kampanj_slut_datum} kampanjPris: {self.kampanj_pris}"  # noqa: E501

    