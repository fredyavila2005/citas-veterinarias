from logica.excepciones import ErrorCitaNoPermitida
from logica.factura import Factura


# Cita veterinaria. Al crearse queda en estado Programada
class Cita:
    PROGRAMADA = "Programada"
    CANCELADA = "Cancelada"
    ATENDIDA = "Atendida"

    def __init__(self, codigo, fecha, hora, propietario, mascota,
                 veterinario, servicio):
        self._codigo = codigo
        self._fecha = fecha
        self._hora = hora
        self._propietario = propietario
        self._mascota = mascota
        self._veterinario = veterinario
        self._servicio = servicio
        self._estado = Cita.PROGRAMADA
        self._servicios_adicionales = []
        self._factura = None

    @property
    def codigo(self):
        return self._codigo

    @property
    def fecha(self):
        return self._fecha

    @property
    def hora(self):
        return self._hora

    @property
    def propietario(self):
        return self._propietario

    @property
    def mascota(self):
        return self._mascota

    @property
    def veterinario(self):
        return self._veterinario

    @property
    def servicio(self):
        return self._servicio

    @property
    def estado(self):
        return self._estado

    @property
    def factura(self):
        return self._factura

    @property
    def servicios_adicionales(self):
        return list(self._servicios_adicionales)

    # Servicio solicitado + los que se agregaron durante la atencion
    @property
    def servicios_prestados(self):
        return [self._servicio] + self._servicios_adicionales

    # Regla 4: solo se cancela una cita Programada
    # Las citas canceladas no se eliminan, solo cambian de estado
    def cancelar(self):
        if self._estado != Cita.PROGRAMADA:
            raise ErrorCitaNoPermitida(
                f"No se puede cancelar la cita {self._codigo} porque su "
                f"estado es {self._estado}."
            )
        self._estado = Cita.CANCELADA

    # Regla 5: solo se atiende una cita Programada, al atenderla se
    # genera la factura
    def atender(self, servicios_adicionales, numero_factura):
        if self._estado != Cita.PROGRAMADA:
            raise ErrorCitaNoPermitida(
                f"No se puede atender la cita {self._codigo} porque su "
                f"estado es {self._estado}."
            )
        self._servicios_adicionales = list(servicios_adicionales)
        self._estado = Cita.ATENDIDA
        self._factura = Factura(
            numero_factura,
            self._fecha,
            self._propietario,
            self._mascota,
            self.servicios_prestados
        )
        return self._factura

    # Se usa al cargar los datos desde el json
    def restaurar_estado(self, estado, servicios_adicionales, factura):
        self._estado = estado
        self._servicios_adicionales = list(servicios_adicionales)
        self._factura = factura

    def a_diccionario(self):
        factura = None
        if self._factura is not None:
            factura = self._factura.a_diccionario()
        return {
            "codigo": self._codigo,
            "fecha": self._fecha.isoformat(),
            "hora": self._hora.strftime("%H:%M"),
            "cedula_propietario": self._propietario.cedula,
            "nombre_mascota": self._mascota.nombre,
            "cedula_veterinario": self._veterinario.cedula,
            "codigo_servicio": self._servicio.codigo,
            "estado": self._estado,
            "servicios_adicionales": [
                s.codigo for s in self._servicios_adicionales
            ],
            "factura": factura
        }
