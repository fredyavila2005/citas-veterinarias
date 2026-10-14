"""Capa de presentación: interfaz de consola para el sistema de citas veterinarias."""
from logica.excepciones import ErrorClinica


class InterfazConsola:
    def __init__(self, gestor):
        self._gestor = gestor

    def iniciar(self):
        print("\n" + "=" * 55)
        print("  CITAS VETERINARIAS - Sistema de Gestión")
        print("=" * 55)
        while True:
            print("\n--- MENÚ PRINCIPAL ---")
            print("1. Registrar clínica")
            print("2. Registrar veterinario")
            print("3. Registrar servicio")
            print("4. Registrar propietario")
            print("5. Registrar mascota")
            print("6. Programar cita")
            print("7. Cancelar cita")
            print("8. Atender cita y generar factura")
            print("9. Consultar citas por fecha")
            print("10. Consultar historial de mascota")
            print("11. Cargar clínicas de ejemplo")
            print("12. Ejecutar los 5 casos de prueba")
            print("13. Reiniciar (borrar todos los datos)")
            print("0. Salir")
            op = input("\nOpción: ").strip()

            try:
                if op == "1":
                    self._registrar_clinica()
                elif op == "2":
                    self._registrar_veterinario()
                elif op == "3":
                    self._registrar_servicio()
                elif op == "4":
                    self._registrar_propietario()
                elif op == "5":
                    self._registrar_mascota()
                elif op == "6":
                    self._programar_cita()
                elif op == "7":
                    self._cancelar_cita()
                elif op == "8":
                    self._atender_cita()
                elif op == "9":
                    self._consultar_fecha()
                elif op == "10":
                    self._consultar_historial()
                elif op == "11":
                    self._cargar_ejemplo()
                elif op == "12":
                    self._ejecutar_casos()
                elif op == "13":
                    self._gestor.reiniciar()
                    print("Todos los datos fueron borrados.")
                elif op == "0":
                    print("Hasta luego.")
                    break
                else:
                    print("Opción no válida.")
            except ErrorClinica as e:
                print(f"⚠ {e}")
            except ValueError as e:
                print(f"⚠ Dato inválido: {e}")
            except Exception as e:
                print(f"⚠ Error inesperado: {e}")

    def _pedir(self, texto, default=""):
        val = input(f"{texto}{' [' + default + ']' if default else ''}: ").strip()
        return val if val else default

    def _registrar_clinica(self):
        c = self._gestor.registrar_clinica(
            self._pedir("NIT"),
            self._pedir("Nombre"),
            self._pedir("Código DANE"),
            self._pedir("Municipio"),
            self._pedir("Departamento"),
            self._pedir("Dirección"),
            self._pedir("Barrio"),
        )
        print(f"Clínica '{c.nombre()}' registrada.")

    def _registrar_veterinario(self):
        v = self._gestor.registrar_veterinario(
            self._pedir("NIT de la clínica"),
            self._pedir("Cédula"),
            self._pedir("Nombre"),
            self._pedir("Tarjeta profesional"),
        )
        print(f"Veterinario {v.nombre()} registrado.")

    def _registrar_servicio(self):
        s = self._gestor.registrar_servicio(
            self._pedir("NIT de la clínica"),
            self._pedir("Código"),
            self._pedir("Nombre"),
            float(self._pedir("Tarifa", "0") or 0),
        )
        print(f"Servicio {s.nombre()} registrado.")

    def _registrar_propietario(self):
        p = self._gestor.registrar_propietario(
            self._pedir("NIT de la clínica"),
            self._pedir("Cédula"),
            self._pedir("Nombre"),
            self._pedir("Teléfono"),
            self._pedir("Municipio"),
        )
        print(f"Propietario {p.nombre()} registrado.")

    def _registrar_mascota(self):
        m = self._gestor.registrar_mascota(
            self._pedir("NIT de la clínica"),
            self._pedir("Cédula del propietario"),
            self._pedir("Nombre"),
            self._pedir("Especie"),
            self._pedir("Raza"),
            int(self._pedir("Año de nacimiento", "2020") or 2020),
            float(self._pedir("Peso", "0") or 0),
        )
        print(f"Mascota {m.nombre()} registrada.")

    def _programar_cita(self):
        c = self._gestor.programar_cita(
            self._pedir("NIT de la clínica"),
            self._pedir("Cédula del propietario"),
            self._pedir("Nombre de la mascota"),
            self._pedir("Fecha (AAAA-MM-DD)"),
            self._pedir("Hora (HH:MM)"),
            self._pedir("Código del servicio"),
            self._pedir("Cédula del veterinario (vacío = automático)"),
        )
        print(f"Cita {c.codigo()} programada con {c.veterinario().nombre()}.")

    def _cancelar_cita(self):
        c = self._gestor.cancelar_cita(self._pedir("Código de la cita"))
        print(f"Cita {c.codigo()} cancelada.")

    def _atender_cita(self):
        extras = self._pedir("Códigos adicionales separados por coma (vacío si no hay)")
        codigos = [x.strip().upper() for x in extras.split(",") if x.strip()]
        f = self._gestor.atender_cita(self._pedir("Código de la cita"), codigos)
        print(f"Factura {f.numero()} generada. Total: ${f.total():,.0f}".replace(",", "."))

    def _consultar_fecha(self):
        citas = self._gestor.citas_por_fecha(
            self._pedir("NIT de la clínica"),
            self._pedir("Fecha (AAAA-MM-DD)"),
        )
        if not citas:
            print("No hay citas en esa fecha.")
            return
        for c in citas:
            print(f"  {c.codigo()} | {c.hora().strftime('%H:%M')} | {c.mascota().nombre()} | {c.estado()}")

    def _consultar_historial(self):
        citas = self._gestor.historial_mascota(
            self._pedir("NIT de la clínica"),
            self._pedir("Cédula del propietario"),
            self._pedir("Nombre de la mascota"),
        )
        if not citas:
            print("Sin historial.")
            return
        for c in citas:
            print(f"  {c.codigo()} | {c.fecha()} {c.hora().strftime('%H:%M')} | {c.estado()}")

    def _cargar_ejemplo(self):
        n = self._gestor.cargar_datos_ejemplo()
        print(f"Se cargaron {n} clínicas de ejemplo.")

    def _ejecutar_casos(self):
        from logica.casos_prueba import ejecutar_casos_prueba
        resultados = ejecutar_casos_prueba(self._gestor)
        print("\n--- RESULTADOS DE LOS CASOS DE PRUEBA ---")
        for caso, paso, exito, detalle in resultados:
            marca = "OK" if exito else "RECHAZADO"
            print(f"[{marca}] {caso} - {paso}: {detalle}")
