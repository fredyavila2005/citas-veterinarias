from logica.validaciones import convertir_fecha


# Factura que se genera al atender una cita.
# Agregacion: la factura referencia al propietario, la mascota y los servicios
class Factura:
    def __init__(self, numero, fecha, propietario, mascota, servicios):
        self._numero = numero
        self._fecha = fecha
        self._propietario = propietario
        self._mascota = mascota
        self._servicios = list(servicios)

    @property
    def numero(self):
        return self._numero

    @property
    def fecha(self):
        return self._fecha

    @property
    def propietario(self):
        return self._propietario

    @property
    def mascota(self):
        return self._mascota

    @property
    def servicios(self):
        return list(self._servicios)

    # El valor total es la suma de las tarifas de los servicios prestados
    @property
    def total(self):
        total = 0
        for servicio in self._servicios:
            total += servicio.tarifa
        return total

    def a_diccionario(self):
        return {
            "numero": self._numero,
            "fecha": self._fecha.isoformat(),
            "servicios": [s.codigo for s in self._servicios],
            "total": self.total
        }

    @staticmethod
    def desde_diccionario(datos, propietario, mascota, servicios):
        return Factura(
            datos["numero"],
            convertir_fecha(datos["fecha"]),
            propietario,
            mascota,
            servicios
        )
