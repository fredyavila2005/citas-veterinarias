from logica.excepciones import ErrorDuplicado, ErrorNoEncontrado
from logica.mascota import Mascota
from logica.validaciones import texto_no_vacio, solo_digitos


# Propietario de una o varias mascotas.
# Composicion: las mascotas solo existen dentro de su propietario.
class Propietario:
    def __init__(self, cedula, nombre, telefono, municipio):
        self._cedula = solo_digitos(cedula, "cédula del propietario", 6, 10)
        self._nombre = texto_no_vacio(nombre, "nombre del propietario")
        self._telefono = solo_digitos(telefono, "teléfono", 10, 10)
        self._municipio = texto_no_vacio(municipio, "municipio")
        # Diccionario de mascotas: clave = nombre en minuscula
        self._mascotas = {}

    @property
    def cedula(self):
        return self._cedula

    @property
    def nombre(self):
        return self._nombre

    @property
    def telefono(self):
        return self._telefono

    @property
    def municipio(self):
        return self._municipio

    @property
    def mascotas(self):
        return list(self._mascotas.values())

    # Agrega una mascota, un propietario no puede repetir nombres
    def agregar_mascota(self, mascota):
        clave = mascota.nombre.lower()
        if clave in self._mascotas:
            raise ErrorDuplicado(
                f"{self._nombre} ya tiene una mascota llamada "
                f"{mascota.nombre}."
            )
        self._mascotas[clave] = mascota

    def buscar_mascota(self, nombre):
        clave = str(nombre).strip().lower()
        if clave not in self._mascotas:
            raise ErrorNoEncontrado(
                f"{self._nombre} no tiene una mascota llamada {nombre}."
            )
        return self._mascotas[clave]

    def a_diccionario(self):
        return {
            "cedula": self._cedula,
            "nombre": self._nombre,
            "telefono": self._telefono,
            "municipio": self._municipio,
            "mascotas": [m.a_diccionario() for m in self.mascotas]
        }

    @staticmethod
    def desde_diccionario(datos):
        propietario = Propietario(
            datos["cedula"],
            datos["nombre"],
            datos["telefono"],
            datos["municipio"]
        )
        for datos_mascota in datos["mascotas"]:
            mascota = Mascota.desde_diccionario(datos_mascota)
            propietario.agregar_mascota(mascota)
        return propietario
