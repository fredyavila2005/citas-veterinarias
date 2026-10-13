from logica.validaciones import texto_no_vacio, numero_mayor_0


# Servicio que ofrece una clinica en su catalogo (consulta, vacuna, etc.)
class Servicio:
    def __init__(self, codigo, nombre, tarifa):
        self._codigo = texto_no_vacio(codigo, "código del servicio").upper()
        self._nombre = texto_no_vacio(nombre, "nombre del servicio")
        self._tarifa = numero_mayor_0(tarifa, "tarifa")

    @property
    def codigo(self):
        return self._codigo

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa(self):
        return self._tarifa

    # Convierte el objeto en diccionario para guardarlo en el json
    def a_diccionario(self):
        return {
            "codigo": self._codigo,
            "nombre": self._nombre,
            "tarifa": self._tarifa
        }

    # Reconstruye el objeto a partir del diccionario del json
    @staticmethod
    def desde_diccionario(datos):
        return Servicio(datos["codigo"], datos["nombre"], datos["tarifa"])
