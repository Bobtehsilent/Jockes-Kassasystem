# c. Discount Campaigns (Class: DiscountCampaign)
  # - Create a class to handle discount campaigns.
   #- Include attributes like campaign name, discount percentage, applicable products, and expiration date.
   #- Implement methods for creating and managing discount campaigns.
from datetime import datetime
class Kampanj:
    def __init__(self, kampanjNamn, kampanjPris, kampanjStartDatum, kampanjSlutDatum):
        self.__kampanjNamn = kampanjNamn
        self.__kampanjPris = kampanjPris
        self.__kampanjStartDatum = datetime.strptime(kampanjStartDatum, '%Y-%m-%d')
        self.__kampanjSlutDatum = datetime.strptime(kampanjSlutDatum, '%Y-%m-%d')

        if kampanjPris <= 0:
            raise ValueError("Kampanj priset måste vara positivt")
        if self.__kampanjStartDatum >= self.__kampanjSlutDatum:
            raise ValueError("Kampanjen måste ta slut efter startdatumet")
    @property
    def kampanjNamn(self):
        return self.__kampanjNamn
    @kampanjNamn.setter
    def kampanjNamn(self, nyttKampanjNamn):
        self.__kampanjNamn = nyttKampanjNamn
    @property
    def kampanjPris(self):
        return self.__kampanjPris
    @kampanjPris.setter
    def kampanjPris(self, nyttKampanjPris):
        self.__kampanjPris = nyttKampanjPris
    @property
    def kampanjStartDatum(self):
        return self.__kampanjStartDatum
    @kampanjStartDatum.setter
    def kampanjStartDatum(self, nyttStartDatum):
        self.__kampanjStartDatum = nyttStartDatum
    @property
    def kampanjSlutDatum(self):
        return self.__kampanjSlutDatum
    @kampanjSlutDatum.setter
    def kampanjSlutDatum(self, nyttSlutDatum):
        self.__kampanjSlutDatum = nyttSlutDatum
    
    def är_aktiv(self):
        idag = datetime.today()
        return self.kampanjStartDatum <= idag <= self.kampanjSlutDatum
    def kampanjdagar_kvar(self):
        if self.är_aktiv():
            dagar_kvar = (self.kampanjSlutDatum - datetime.today()).days
            return dagar_kvar
        else:
            return 0
    def räkna_rabatt(self, original_pris):
        return original_pris * (1 - (self.kampanjPris // 100))
    def formatera(self):
        return {
            'kampanjNamn' : self.kampanjNamn,
            'kampanjPris' : self.kampanjPris,
            'kampanjStartDatum': self.kampanjStartDatum,
            'kampanjSlutDatum' : self.kampanjSlutDatum
        }
    def __str__(self):
        return f"kampanjNamn: {self.kampanjNamn} kampanjPris: {self.kampanjPris} StartDatum: {self.kampanjStartDatum} SlutDatum: {self.kampanjSlutDatum}"  # noqa: E501

    