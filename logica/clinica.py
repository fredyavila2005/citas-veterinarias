from logica.cita import Cita
from logica.excepciones import (
    ErrorDuplicado, ErrorNoEncontrado, ErrorDisponibilidad
)
from logica.factura import Factura
from logica.propietario import Propietario
from logica.servicio import Servicio
from logica.validaciones import (
    texto_no_vacio, solo_digitos, validar_nit, convertir_fecha, convertir_hora
)
from logica.veterinario import Veterinario


# Clinica veterinaria que contrata el software.
# Tiene veterinarios, catalogo de servicios, propietarios y citas.
class Clinica:
    def __init__(self, nit, nombre, codigo_dane, municipio, departamento,
                 direccion, barrio):
        self._nit = validar_nit(nit)
        self._nombre = texto_no_vacio(nombre, "nombre de la clínica")
        self._codigo_dane = solo_digitos(codigo_dane, "código DANE", 5, 5)
        self._municipio = texto_no_vacio(municipio, "municipio")
        self._departamento = texto_no_vacio(departamento, "departamento")
        self._direccion = texto_no_vacio(direccion, "dirección")
        self._barrio = texto_no_vacio(barrio, "barrio")
        # Colecciones: se guardan en diccionarios con la clave de busqueda
        self._veterinarios = {}
        self._servicios = {}
        self._propietarios = {}
        self._citas = {}

    @property
    def nit(self):
        return self._nit

    @property
    def nombre(self):
        return self._nombre

    @property
    def codigo_dane(self):
        return self._codigo_dane

    @property
    def municipio(self):
        return self._municipio

    @property
    def departamento(self):
        return self._departamento

    @property
    def direccion(self):
        return self._direccion

    @property
    def barrio(self):
        return self._barrio

    @property
    def veterinarios(self):
        return list(self._veterinarios.values())

    @property
    def servicios(self):
        return list(self._servicios.values())

    @property
    def propietarios(self):
        return list(self._propietarios.values())

    @property
    def citas(self):
        return list(self._citas.values())

    # Regla 7: no se repite la cedula de un veterinario en la misma clinica
    def agregar_veterinario(self, veterinario):
        if veterinario.cedula in self._veterinarios:
            raise ErrorDuplicado(
                f"Ya existe un veterinario con cédula {veterinario.cedula} "
                f"en {self._nombre}."
            )
        self._veterinarios[veterinario.cedula] = veterinario

    # Regla 7: no se repite el codigo de un servicio en la misma clinica
    def agregar_servicio(self, servicio):
        if servicio.codigo in self._servicios:
            raise ErrorDuplicado(
                f"Ya existe un servicio con código {servicio.codigo} "
                f"en {self._nombre}."
            )
        self._servicios[servicio.codigo] = servicio

    # Regla 7: no se repite la cedula de un propietario en la misma clinica
    def agregar_propietario(self, propietario):
        if propietario.cedula in self._propietarios:
            raise ErrorDuplicado(
                f"Ya existe un propietario con cédula {propietario.cedula} "
                f"en {self._nombre}."
            )
        self._propietarios[propietario.cedula] = propietario

    def buscar_veterinario(self, cedula):
        if cedula not in self._veterinarios:
            raise ErrorNoEncontrado(
                f"No existe un veterinario con cédula {cedula} "
                f"en {self._nombre}."
            )
        return self._veterinarios[cedula]

    def buscar_servicio(self, codigo):
        codigo = str(codigo).strip().upper()
        if codigo not in self._servicios:
            raise ErrorNoEncontrado(
                f"No existe el servicio {codigo} en {self._nombre}."
            )
        return self._servicios[codigo]

    def buscar_propietario(self, cedula):
        cedula = str(cedula).strip()
        if cedula not in self._propietarios:
            raise ErrorNoEncontrado(
                f"No existe un propietario con cédula {cedula} "
                f"en {self._nombre}."
            )
        return self._propietarios[cedula]

    def buscar_cita(self, codigo):
        codigo = str(codigo).strip().upper()
        if codigo not in self._citas:
            raise ErrorNoEncontrado(
                f"No existe la cita {codigo} en {self._nombre}."
            )
        return self._citas[codigo]

    # Busca la cita no cancelada que tiene el veterinario en esa fecha y hora.
    # Una cita atendida tambien ocupa el horario, por eso solo se descartan
    # las canceladas.
    def _cita_del_veterinario(self, veterinario, fecha, hora):
        for cita in self._citas.values():
            if (cita.veterinario is veterinario
                    and cita.fecha == fecha
                    and cita.hora == hora
                    and cita.estado != Cita.CANCELADA):
                return cita
        return None

    # Regla 3: una mascota no puede tener dos citas en la misma fecha y hora
    def validar_mascota_libre(self, mascota, fecha, hora):
        for cita in self._citas.values():
            if (cita.mascota is mascota
                    and cita.fecha == fecha
                    and cita.hora == hora
                    and cita.estado != Cita.CANCELADA):
                raise ErrorDisponibilidad(
                    f"{mascota.nombre} ya tiene la cita {cita.codigo} "
                    f"en esa fecha y hora."
                )

    # Regla 2: un veterinario no puede tener dos citas a la misma hora.
    # Si el usuario no escoge veterinario, la clinica asigna el primero
    # que este disponible.
    def asignar_veterinario(self, fecha, hora, cedula=""):
        if cedula:
            veterinario = self.buscar_veterinario(cedula)
            cita = self._cita_del_veterinario(veterinario, fecha, hora)
            if cita is not None:
                raise ErrorDisponibilidad(
                    f"{veterinario.nombre} ya tiene la cita {cita.codigo} "
                    f"en esa fecha y hora."
                )
            return veterinario
        for veterinario in self._veterinarios.values():
            if self._cita_del_veterinario(veterinario, fecha, hora) is None:
                return veterinario
        raise ErrorDisponibilidad(
            "No hay veterinarios disponibles en esa fecha y hora."
        )

    def registrar_cita(self, cita):
        self._citas[cita.codigo] = cita

    # Citas de un dia ordenadas por hora
    def citas_por_fecha(self, fecha):
        citas = [c for c in self._citas.values() if c.fecha == fecha]
        return sorted(citas, key=lambda c: c.hora)

    # Historial de una mascota ordenado por fecha y hora
    def historial_mascota(self, mascota):
        citas = [c for c in self._citas.values() if c.mascota is mascota]
        return sorted(citas, key=lambda c: (c.fecha, c.hora))

    def a_diccionario(self):
        return {
            "nit": self._nit,
            "nombre": self._nombre,
            "codigo_dane": self._codigo_dane,
            "municipio": self._municipio,
            "departamento": self._departamento,
            "direccion": self._direccion,
            "barrio": self._barrio,
            "veterinarios": [v.a_diccionario() for v in self.veterinarios],
            "servicios": [s.a_diccionario() for s in self.servicios],
            "propietarios": [p.a_diccionario() for p in self.propietarios],
            "citas": [c.a_diccionario() for c in self.citas]
        }

    # Reconstruye la clinica completa (con sus citas) desde el json
    @staticmethod
    def desde_diccionario(datos):
        clinica = Clinica(
            datos["nit"],
            datos["nombre"],
            datos["codigo_dane"],
            datos["municipio"],
            datos["departamento"],
            datos["direccion"],
            datos["barrio"]
        )
        for d in datos["servicios"]:
            clinica.agregar_servicio(Servicio.desde_diccionario(d))
        for d in datos["veterinarios"]:
            clinica.agregar_veterinario(Veterinario.desde_diccionario(d))
        for d in datos["propietarios"]:
            clinica.agregar_propietario(Propietario.desde_diccionario(d))
        for d in datos["citas"]:
            clinica._restaurar_cita(d)
        return clinica

    # Reconstruye una cita y sus relaciones con los objetos ya cargados
    def _restaurar_cita(self, d):
        propietario = self.buscar_propietario(d["cedula_propietario"])
        mascota = propietario.buscar_mascota(d["nombre_mascota"])
        cita = Cita(
            d["codigo"],
            convertir_fecha(d["fecha"]),
            convertir_hora(d["hora"]),
            propietario,
            mascota,
            self.buscar_veterinario(d["cedula_veterinario"]),
            self.buscar_servicio(d["codigo_servicio"])
        )
        adicionales = [
            self.buscar_servicio(c) for c in d["servicios_adicionales"]
        ]
        factura = None
        if d["factura"] is not None:
            factura = Factura.desde_diccionario(
                d["factura"], propietario, mascota, cita.servicios_prestados
                + adicionales
            )
        cita.restaurar_estado(d["estado"], adicionales, factura)
        self._citas[cita.codigo] = cita
