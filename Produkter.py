# a. Products (Class: Product)
 # - Each product should have attributes like name, price, quantity in stock, and a unique identifier.
 #  - Create methods for adding products, updating quantities, and displaying product information.

class Produkt:
    def __init__(self, produkt_id:str,produkt_namn:str, produkt_pris:float) -> None:  # noqa: E501
        self.__produkt_id = produkt_id
        self.__produkt_pris = float(produkt_pris)
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
        self.__produkt_pris = nytt_pris
    @property
    def produkt_id(self):
        return self.__produkt_id
    @produkt_id.setter
    def produkt_id(self, nytt_id):
        self.__produkt_id = nytt_id

    def formattera(self):
        return {
            'produkt_id':self.produkt_id,
            'produkt_namn':self.produkt_namn,
            'produkt_pris':self.produkt_pris,
        }
    def __str__(self) -> str:
        return f"Id: {self.produkt_id} Namn: {self.produkt_namn} Pris: {self.produkt_pris}"



