import datetime
from Produkter import Produkt

class KvittoRad:
    def __init__(self, produktNamn:str, count:int, perPris:float, kampanjDatum:str, kampanjPris:float):  # noqa: E501
        self.__produktNamn = produktNamn
        self.__count = count
        self.__perPris = perPris
        self.__kampanjDatum = kampanjDatum
        self.__kampanjPris = kampanjPris
    def Addcount(self,count):
         self.__count = self.__count + count
    def GetTotal(self):
        return self.__count * self.__perPris
    def GetName(self):
        return self.__produktNamn
    def GetCount(self):
        return self.__count
    def GetPerPris(self):
        return self.__perPris
    def GetKampanjdatum(self):
        return self.__kampanjDatum
    def GetKampanjPris(self):
        return self.__kampanjPris
    def GetTotalkampanj(self):
        return self.__count * self.__kampanjPris

class Kvitto:
    def __init__(self) -> None:
        self.__Datum = datetime.date.today()
        self.__kvittoRad = []
    def TotalSumma(self):
        sum = 0
        for row in self.__kvittoRad:
            sum = sum + row.GetTotal()
        return sum
    def GetDatum(self):
        return self.__Datum
    def LäggTill(self, produktNamn:str, count:int, perPris:float, kampanjDatum, kampanjPris):
        kvittoRad = KvittoRad(produktNamn, count, perPris , kampanjDatum, kampanjPris)
        for prdukt in self.__kvittoRad:
            if prdukt.GetName() == kvittoRad.GetName():
                prdukt.Addcount()
                return
        getDatum = kampanjDatum
        if getDatum != " ":
            parts = getDatum.split(",")
            start = datetime.strptime(parts[0],"%Y-%m-%d".date())
            end = datetime.strptime(parts[1],"%Y-%m-%d".date())
            currentDate = datetime.now().date()
            if start <= currentDate <= end:
                kvittoRad = KvittoRad(produktNamn, count, kampanjDatum, kampanjPris, perPris)
                self.__kvittoRad.append(kvittoRad)
                return
        self.__kvittoRad.append(kvittoRad)
    def getKvittorad(self):
        return self.__kvittoRad
    def KollaKampanjInomDatum(self, getDatum1, getDatum2):
        start = datetime.strptime(getDatum1,"%Y-%m-%d").date()
        end = datetime.strptime(getDatum2,"%Y-%m-%d").date()
        currentDatum = datetime.now().date()
        if start <= currentDatum <= end:
            return True
        return False
