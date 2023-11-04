from datetime import datetime
#Klass för att skapa objekten kring kampanjer, samt validering av datum.
class Kampanj:
    def __init__(self, kampanj_namn, produkt_id, kampanj_pris, 
                 kampanj_start_datum, kampanj_slut_datum):
        self.__kampanj_namn = kampanj_namn
        self.__produkt_id = produkt_id
        self.__kampanj_pris = kampanj_pris
        self.__kampanj_start_datum = self.analysera_och_validera(kampanj_start_datum)
        self.__kampanj_slut_datum = self.analysera_och_validera(kampanj_slut_datum)
        if self.__kampanj_slut_datum < self.__kampanj_start_datum:
            raise ValueError("Slutdatum kan inte vara före startdatum")

    @property
    def kampanj_namn(self):
        return self.__kampanj_namn

    @kampanj_namn.setter
    def kampanj_namn(self, nytt_kampanj_namn):
        self.__kampanj_namn = nytt_kampanj_namn

    @property
    def produkt_id(self):
        return self.__produkt_id

    @produkt_id.setter
    def produkt_id(self, nytt_produkt_id):
        self.__produkt_id = nytt_produkt_id

    @property
    def kampanj_pris(self):
        return self.__kampanj_pris

    @kampanj_pris.setter
    def kampanj_pris(self, nytt_kampanj_pris):
        if not isinstance(nytt_kampanj_pris, (int,float)) or nytt_kampanj_pris <= 0:
            raise ValueError("Kampanjpris måste vara ett positivt tal")
        self.__kampanj_pris = nytt_kampanj_pris

    @property
    def kampanj_start_datum(self):
        return self.__kampanj_start_datum

    @kampanj_start_datum.setter
    def kampanj_start_datum(self, nytt_start_datum):
        self.__kampanj_start_datum = self.analysera_och_validera(nytt_start_datum)

    @property
    def kampanj_slut_datum(self):
        return self.__kampanj_slut_datum

    @kampanj_slut_datum.setter
    def kampanj_slut_datum(self, nytt_slut_datum):
        self.__kampanj_slut_datum = self.analysera_och_validera(nytt_slut_datum)
    
    @staticmethod
    def analysera_och_validera(datumstr):
        if isinstance(datumstr, datetime):
            return datumstr
        elif isinstance(datumstr, str):
            format = "%Y-%m-%d"
            try:
                return datetime.strptime(datumstr, format)
            except ValueError:
                print("Error: Ogiltigt format. Försök igen.")
                return None
        else:
            print("Received an unexpected type, raising ValueError.")
            raise ValueError("Oväntad typ: förväntar str eller datetime")

    def till_dict(self):    #Formatterar ner kampanjinformationen för att sparas i en jsonfil
        return {
            'kampanj_namn': self.kampanj_namn,
            'produkt_id': self.produkt_id,
            'kampanj_pris': self.kampanj_pris,
            'kampanj_start_datum': self.kampanj_start_datum.strftime("%Y-%m-%d"),
            'kampanj_slut_datum': self.kampanj_slut_datum.strftime("%Y-%m-%d")
        }

    def __str__(self):
        return (f"Startdatum: {self.kampanj_start_datum} Slutdatum: "
            f"{self.kampanj_slut_datum} kampanjpris: {self.kampanj_pris}")
