from logica.validaciones import texto_no_vacio, solo_digitos


# Veterinario que trabaja en una clinica
class Veterinario:
    def __init__(self, cedula, nombre, tarjeta_profesional):
        self._cedula = solo_digitos(cedula, "cédula del veterinario", 6, 10)
        self._nombre = texto_no_vacio(nombre, "nombre del veterinario")
        self._tarjeta_profesional = texto_no_vacio(
            tarjeta_profesional, "tarjeta profesional"
        ).upper()

    @property
    def cedula(self):
        return self._cedula

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarjeta_profesional(self):
        return self._tarjeta_profesional

    def a_diccionario(self):
        return {
            "cedula": self._cedula,
            "nombre": self._nombre,
            "tarjeta_profesional": self._tarjeta_profesional
        }

    @staticmethod
    def desde_diccionario(datos):
        return Veterinario(
            datos["cedula"], datos["nombre"], datos["tarjeta_profesional"]
        )
