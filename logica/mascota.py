from logica.validaciones import texto_no_vacio, numero_mayor_0, anio_valido


# Mascota de un propietario
class Mascota:
    def __init__(self, nombre, especie, raza, anio_nacimiento, peso):
        self._nombre = texto_no_vacio(nombre, "nombre de la mascota")
        self._especie = texto_no_vacio(especie, "especie")
        self._raza = texto_no_vacio(raza, "raza")
        self._anio_nacimiento = anio_valido(anio_nacimiento)
        self._peso = numero_mayor_0(peso, "peso")

    @property
    def nombre(self):
        return self._nombre

    @property
    def especie(self):
        return self._especie

    @property
    def raza(self):
        return self._raza

    @property
    def anio_nacimiento(self):
        return self._anio_nacimiento

    @property
    def peso(self):
        return self._peso

    def a_diccionario(self):
        return {
            "nombre": self._nombre,
            "especie": self._especie,
            "raza": self._raza,
            "anio_nacimiento": self._anio_nacimiento,
            "peso": self._peso
        }

    @staticmethod
    def desde_diccionario(datos):
        return Mascota(
            datos["nombre"],
            datos["especie"],
            datos["raza"],
            datos["anio_nacimiento"],
            datos["peso"]
        )
