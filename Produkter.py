class Produkt:
    def __init__(self, produkt_id:str,produkt_namn:str, produkt_pris:float, pris_typ:str):
        self.__produkt_id = produkt_id
        self.__produkt_pris = produkt_pris
        self.__produkt_namn = produkt_namn
        self.__pris_typ = pris_typ
    @property
    def produkt_namn(self):
        return self.__produkt_namn
    @produkt_namn.setter
    def produkt_namn(self, nytt_namn):
        self.__produkt_namn = nytt_namn
    @property
    def produkt_pris(self):
        return self.__produkt_pris
    @produkt_pris.setter
    def produkt_pris(self, nytt_pris):
        try:
            self.__produkt_pris = float(nytt_pris)
        except ValueError:
            print("Ogiltigt prisformat, priset måste vara en siffra.")
    @property
    def produkt_id(self):
        return self.__produkt_id
    @produkt_id.setter
    def produkt_id(self, nytt_id):
        self.__produkt_id = nytt_id
    @property
    def produkt_pris_typ(self):
        return self.__pris_typ
    @produkt_pris_typ.setter
    def produkt_pris_typ(self, ny_pris_typ):
        self.__pris_typ = ny_pris_typ

    def till_dict(self):
        """
        Skapar en dictionary formattering av produkt objekten
        för att spara till en .json

        Returns:
            dict: en dictionary med nycklarna 'produkt_id', 'produkt_namn' 
            och produkt_pris och deras attribut som värden
        """
        return {
            'produkt_id':self.produkt_id,
            'produkt_namn':self.produkt_namn,
            'produkt_pris':self.produkt_pris,
            'produkt_pris_typ':self.produkt_pris_typ
        }
    def __str__(self) -> str:
        return (f"Produkt id: {self.produkt_id} | Produkt namn: {self.produkt_namn} "
            f"| Produkt Pris: {self.produkt_pris} SEK")
