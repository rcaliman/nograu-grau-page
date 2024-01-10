class Calculator:
    def __init__(self, cavalo, esterno, braco, email, csrfmiddlewaretoken=None, id=None, data=None):
        self.cavalo = float(cavalo[0]) if isinstance(cavalo, list) else cavalo
        self.esterno = float(esterno[0]) if isinstance(esterno, list) else esterno
        self.braco = float(braco[0]) if isinstance(braco, list) else braco
        self.email = email[0] if isinstance (email, list) else email
        self.csrfmiddlewaretoken = csrfmiddlewaretoken
        self.id = id
        self.data = data


    def calcula_tronco(self):
        return round((self.esterno - self.cavalo),1)

    def calcula_quadro_speed(self):
        return round((self.cavalo * 0.67),1)

    def calcula_quadro_mtb(self):
        return round(((self.cavalo * 0.67 - 10) * 0.393700787),1)

    def calcula_altura_selim(self):
        return round((self.cavalo * 0.883),1)
    
    def calcula_top_tube_efetivo(self):
        return round((((self.esterno - self.cavalo + self.braco)/2)+4),1)

    def result(self):
        return {
            'cavalo': self.cavalo,
            'esterno': self.esterno,
            'braco': self.braco,
            'tronco': self.calcula_tronco(),
            'email': self.email,
            'quadro_speed': self.calcula_quadro_speed(),
            'quadro_mtb': self.calcula_quadro_mtb(),
            'altura_selim': self.calcula_altura_selim(),
            'top_tube_efetivo': self.calcula_top_tube_efetivo(),
            'data': self.data,
        }