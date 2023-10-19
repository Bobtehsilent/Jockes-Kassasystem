class Produkt:
    def __init__(self, produkt_id:str,produkt_namn:str, produkt_pris:float):
        self.__produkt_id = produkt_id
        self.__produkt_pris = produkt_pris
        self.__produkt_namn = produkt_namn
        
        if self.__produkt_pris < 0:
            raise ValueError("Varans pris måste vara positiv.")
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
        if not isinstance(nytt_pris, (int, float)) or nytt_pris < 0:
            raise ValueError("Error: Pris måste vara ett positivt heltal")
        self.__produkt_pris = nytt_pris
    @property
    def produkt_id(self):
        return self.__produkt_id
    @produkt_id.setter
    def produkt_id(self, nytt_id):
        self.__produkt_id = nytt_id

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
        }
    def __str__(self) -> str:
        return (f"Produkt id: {self.produkt_id} | Produkt namn: {self.produkt_namn} "
            f"| Produkt Pris: {self.produkt_pris} SEK")
