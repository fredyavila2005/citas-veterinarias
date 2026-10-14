from datos.datos_ejemplo import CLINICAS_EJEMPLO
from logica.cita import Cita
from logica.clinica import Clinica
from logica.excepciones import ErrorDuplicado, ErrorNoEncontrado
from logica.mascota import Mascota
from logica.propietario import Propietario
from logica.servicio import Servicio
from logica.validaciones import (
    texto_no_vacio, convertir_fecha, convertir_hora, formatear_codigo
)
from logica.veterinario import Veterinario


# Clase que coordina toda la logica del negocio.
# La presentacion solo habla con esta clase y ella se encarga de las clinicas
# y de guardar los cambios en el repositorio (capa de datos).
class GestorClinicas:
    def __init__(self, repositorio):
        self._repositorio = repositorio
        # Diccionario de clinicas: clave = NIT
        self._clinicas = {}
        # Los codigos de citas y facturas son consecutivos en todo el sistema
        self._contador_citas = 0
        self._contador_facturas = 0
        self._cargar()

    @property
    def clinicas(self):
        return list(self._clinicas.values())

    # ------------------------------------------------------------------
    # Persistencia
    # ------------------------------------------------------------------
    def _guardar(self):
        datos = {
            "contador_citas": self._contador_citas,
            "contador_facturas": self._contador_facturas,
            "clinicas": [c.a_diccionario() for c in self.clinicas]
        }
        self._repositorio.guardar(datos)

    def _cargar(self):
        datos = self._repositorio.cargar()
        if not datos:
            return
        self._contador_citas = datos["contador_citas"]
        self._contador_facturas = datos["contador_facturas"]
        for datos_clinica in datos["clinicas"]:
            clinica = Clinica.desde_diccionario(datos_clinica)
            self._clinicas[clinica.nit] = clinica

    # Borra toda la informacion (sirve para repetir las pruebas)
    def reiniciar(self):
        self._clinicas = {}
        self._contador_citas = 0
        self._contador_facturas = 0
        self._guardar()

    # ------------------------------------------------------------------
    # Registro
    # ------------------------------------------------------------------
    def buscar_clinica(self, nit):
        nit = texto_no_vacio(nit, "clínica").strip()
        if nit not in self._clinicas:
            raise ErrorNoEncontrado(f"No existe la clínica con NIT {nit}.")
        return self._clinicas[nit]

    # Funcionalidad 1: registrar una clinica
    def registrar_clinica(self, nit, nombre, codigo_dane, municipio,
                          departamento, direccion, barrio):
        clinica = Clinica(
            nit, nombre, codigo_dane, municipio, departamento, direccion,
            barrio
        )
        # Regla 7: no pueden existir dos clinicas con el mismo NIT
        if clinica.nit in self._clinicas:
            raise ErrorDuplicado(
                f"Ya existe una clínica con NIT {clinica.nit}."
            )
        self._clinicas[clinica.nit] = clinica
        self._guardar()
        return clinica

    # Funcionalidad 2: registrar veterinarios y servicios
    def registrar_veterinario(self, nit, cedula, nombre, tarjeta):
        clinica = self.buscar_clinica(nit)
        veterinario = Veterinario(cedula, nombre, tarjeta)
        clinica.agregar_veterinario(veterinario)
        self._guardar()
        return veterinario

    def registrar_servicio(self, nit, codigo, nombre, tarifa):
        clinica = self.buscar_clinica(nit)
        servicio = Servicio(codigo, nombre, tarifa)
        clinica.agregar_servicio(servicio)
        self._guardar()
        return servicio

    # Funcionalidad 3: registrar propietario y sus mascotas
    def registrar_propietario(self, nit, cedula, nombre, telefono,
                              municipio):
        clinica = self.buscar_clinica(nit)
        propietario = Propietario(cedula, nombre, telefono, municipio)
        clinica.agregar_propietario(propietario)
        self._guardar()
        return propietario

    def registrar_mascota(self, nit, cedula_propietario, nombre, especie,
                          raza, anio_nacimiento, peso):
        clinica = self.buscar_clinica(nit)
        propietario = clinica.buscar_propietario(cedula_propietario)
        mascota = Mascota(nombre, especie, raza, anio_nacimiento, peso)
        propietario.agregar_mascota(mascota)
        self._guardar()
        return mascota

    # ------------------------------------------------------------------
    # Citas
    # ------------------------------------------------------------------
    # Funcionalidad 4: programar una cita
    def programar_cita(self, nit, cedula_propietario, nombre_mascota,
                       fecha_texto, hora_texto, codigo_servicio,
                       cedula_veterinario=""):
        clinica = self.buscar_clinica(nit)
        propietario = clinica.buscar_propietario(cedula_propietario)
        mascota = propietario.buscar_mascota(nombre_mascota)
        servicio = clinica.buscar_servicio(codigo_servicio)
        fecha = convertir_fecha(fecha_texto)
        hora = convertir_hora(hora_texto)

        # Primero se validan las reglas, el codigo solo se gasta si la
        # cita queda programada
        clinica.validar_mascota_libre(mascota, fecha, hora)
        veterinario = clinica.asignar_veterinario(
            fecha, hora, cedula_veterinario
        )

        codigo = formatear_codigo("CIT", self._contador_citas + 1)
        cita = Cita(
            codigo, fecha, hora, propietario, mascota, veterinario, servicio
        )
        clinica.registrar_cita(cita)
        self._contador_citas += 1
        self._guardar()
        return cita

    # Busca una cita por su codigo en todas las clinicas
    def buscar_cita(self, codigo):
        codigo = texto_no_vacio(codigo, "código de la cita").upper()
        for clinica in self.clinicas:
            try:
                return clinica.buscar_cita(codigo)
            except ErrorNoEncontrado:
                pass
        raise ErrorNoEncontrado(f"No existe la cita {codigo}.")

    # Funcionalidad 5: cancelar una cita
    # Funcionalidad 5: cancelar una cita
    def cancelar_cita(self, codigo, fecha_cancelacion=None):
        cita = self.buscar_cita(codigo)
        cita.cancelar(fecha_cancelacion)
        self._guardar()
        return cita

    # Funcionalidad 6: atender una cita, agregar servicios y facturar
    def atender_cita(self, codigo, codigos_adicionales=None):
        cita = self.buscar_cita(codigo)
        clinica = self._clinica_de_cita(cita)
        servicios_adicionales = []
        for codigo_servicio in codigos_adicionales or []:
            servicio = clinica.buscar_servicio(codigo_servicio)
            if servicio is cita.servicio:
                continue
            servicios_adicionales.append(servicio)
        numero = formatear_codigo("FAC", self._contador_facturas + 1)
        factura = cita.atender(servicios_adicionales, numero)
        self._contador_facturas += 1
        self._guardar()
        return factura

    def _clinica_de_cita(self, cita):
        for clinica in self.clinicas:
            if cita in clinica.citas:
                return clinica
        raise ErrorNoEncontrado(f"No existe la cita {cita.codigo}.")

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    # Funcionalidad 7: citas de una clinica en una fecha
    def citas_por_fecha(self, nit, fecha_texto):
        clinica = self.buscar_clinica(nit)
        return clinica.citas_por_fecha(convertir_fecha(fecha_texto))

    # Funcionalidad 8: historial de citas de una mascota
    def historial_mascota(self, nit, cedula_propietario, nombre_mascota):
        clinica = self.buscar_clinica(nit)
        propietario = clinica.buscar_propietario(cedula_propietario)
        mascota = propietario.buscar_mascota(nombre_mascota)
        return clinica.historial_mascota(mascota)

    # ------------------------------------------------------------------
    # Datos de ejemplo
    # ------------------------------------------------------------------
    # Carga las clinicas del enunciado, devuelve cuantas clinicas nuevas
    # se cargaron (las que ya existen se omiten)
    def cargar_datos_ejemplo(self):
        cargadas = 0
        for datos in CLINICAS_EJEMPLO:
            if datos["nit"] in self._clinicas:
                continue
            self.registrar_clinica(
                datos["nit"], datos["nombre"], datos["codigo_dane"],
                datos["municipio"], datos["departamento"],
                datos["direccion"], datos["barrio"]
            )
            for cedula, nombre, tarjeta in datos["veterinarios"]:
                self.registrar_veterinario(
                    datos["nit"], cedula, nombre, tarjeta
                )
            for codigo, nombre, tarifa in datos["servicios"]:
                self.registrar_servicio(datos["nit"], codigo, nombre, tarifa)
            for prop in datos.get("propietarios", []):
                self.registrar_propietario(
                    datos["nit"], prop["cedula"], prop["nombre"],
                    prop["telefono"], prop["municipio"]
                )
                for nombre, especie, raza, anio, peso in prop.get("mascotas", []):
                    self.registrar_mascota(
                        datos["nit"], prop["cedula"], nombre, especie,
                        raza, anio, peso
                    )
            cargadas += 1
        return cargadas


    def eliminar_cita(self, codigo):
        """Elimina una cita del sistema (útil para limpiar pruebas)."""
        cita = self.buscar_cita(codigo)
        for clinica in self.clinicas:
            if codigo in clinica._citas:
                del clinica._citas[codigo]
                self._guardar()
                return True
        return False
